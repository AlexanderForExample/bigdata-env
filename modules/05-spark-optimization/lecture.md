# 05 - Spark optimization

## Goal
- научить студентов не просто писать рабочий Spark-код, а уметь анализировать его производительность
- показать связь между logical plan, physical plan, shuffle и cluster configuration
- разобрать не только кодовые оптимизации, но и конфигурационные параметры Spark

## Why optimization is a separate topic
- Spark-пайплайн может быть логически корректным и при этом непригодным для production из-за времени выполнения или стоимости
- в distributed execution цена ошибки выше: лишний shuffle, плохой join strategy или неверное число partition быстро превращаются в долгий и дорогой job
- инженер должен уметь отвечать не только на вопрос "правильный ли результат", но и на вопрос "почему это работает медленно"

## Technology deep dive

### Logical plan vs physical plan
- logical plan описывает, что именно нужно получить
- physical plan описывает, как Spark реально это будет исполнять
- `explain()` нужен именно для чтения физического плана: там видны joins, exchanges, scan strategy и adaptive optimization

### Narrow and wide transformations
- narrow transformations не требуют перераспределения данных между partition и обычно дешевле
- wide transformations приводят к shuffle: данные должны быть переразбросаны между executors
- `groupBy`, `distinct`, некоторые `join` и `orderBy` почти всегда тянут shuffle

### Shuffle
- shuffle - одна из самых дорогих частей Spark execution
- он требует сериализации, записи на диск, network transfer и повторного чтения данных
- любая оптимизация, которая уменьшает объем данных до shuffle, часто дает заметный выигрыш

### Data skew
- skew возникает, когда ключи распределены неравномерно и одна partition получает сильно больше данных, чем другие
- это приводит к straggler tasks: большинство задач уже закончило работу, а одна-две все еще крутятся
- skew особенно опасен в join и groupBy на "тяжелых" ключах

### Join strategies
- sort-merge join - типовая стратегия для больших наборов данных
- broadcast hash join эффективен, когда одна таблица маленькая и ее можно раздать на все executors
- неправильная стратегия join может сделать pipeline сильно медленнее даже при корректном результате

### Cache and persist
- `cache` полезен, если один и тот же DataFrame читается несколько раз в рамках одного pipeline
- кешировать все подряд вредно: это расходует память и может ухудшить выполнение
- инженер должен понимать, почему он кеширует набор данных и где этот cache потом действительно используется

## Configuration matters

### `spark.sql.shuffle.partitions`
- задает количество partition после shuffle-операций в Spark SQL/DataFrame API
- слишком большое значение создает много маленьких задач с overhead на scheduling
- слишком маленькое значение приводит к большим partition и плохому параллелизму
- это один из первых параметров, которые стоит смотреть при тяжелых `groupBy` и `join`

### `spark.default.parallelism`
- базовое число partition для некоторых RDD- и shuffle-related операций
- часто определяется кластером автоматически, но важно понимать, откуда берется baseline parallelism
- если его игнорировать, можно получить неожиданно мало или неожиданно много задач

### `spark.sql.autoBroadcastJoinThreshold`
- определяет максимальный размер маленькой таблицы, которую Spark может broadcast'ить автоматически
- если threshold слишком низкий, Spark не выберет выгодный broadcast join
- если слишком высокий, можно попытаться broadcast'ить слишком крупный справочник и упереться в память

### `spark.sql.adaptive.enabled`
- включает Adaptive Query Execution, то есть возможность менять plan на лету после получения статистики
- часто это must-have для современных Spark job'ов
- без AQE Spark хуже адаптируется к реальному распределению данных и размеру partition

### `spark.sql.adaptive.coalescePartitions.enabled`
- позволяет Spark уменьшать количество partition после shuffle, если фактических данных оказалось меньше ожидаемого
- это снижает overhead на лишние tiny tasks
- особенно полезно, когда входной объем меняется от запуска к запуску

### `spark.sql.adaptive.skewJoin.enabled`
- позволяет Spark обнаруживать skewed partition и обрабатывать их отдельно
- это не серебряная пуля, но важная защита для join-heavy workload
- параметр особенно полезен, когда данные реально имеют hot keys

### `spark.sql.files.maxPartitionBytes`
- управляет тем, сколько байт Spark пытается читать в одну input partition из файловых источников
- влияет на начальный размер задач при чтении больших файлов
- слишком крупные partition ухудшают parallelism, слишком мелкие создают overhead на scheduling

### `spark.executor.memory`
- объем памяти на executor
- если памяти недостаточно, начинаются spill to disk, OOM и деградация производительности
- если задать слишком много памяти на executor, можно потерять в parallelism или не влезть в ресурсы кластера

### `spark.executor.cores`
- число ядер на executor
- слишком много ядер на одном executor может привести к конкуренции за память и I/O
- слишком мало - к излишнему числу executors и большему overhead

### `spark.executor.instances`
- число executors для приложения
- влияет на общий parallelism и footprint приложения в кластере
- этот параметр нельзя рассматривать отдельно от `executor.memory`, `executor.cores` и реальных ресурсов YARN/Kubernetes cluster

## How to reason about optimization
1. Сначала построить baseline.
2. Затем прочитать physical plan и найти реальные bottlenecks.
3. Потом менять по одному фактору: код или конфиг.
4. После каждой правки заново измерять поведение.
5. Фиксировать не только ускорение, но и trade-offs.

## Practice flow
1. Собрать медленный baseline pipeline.
2. Измерить runtime и посмотреть explain plan.
3. Вынести гипотезы по bottlenecks.
4. Применить code-level оптимизации.
5. Применить config-level оптимизации.
6. Сравнить результат и объяснить, почему стало лучше или хуже.

## Suggested implementation scope
- 180-260 строк кода в notebook
- обязательны helper-функции для measurement, explain capture и запуска разных конфигураций
- в решении должны быть baseline, минимум три оптимизации и отдельный блок про конфигурацию Spark

## Expected output
- студент умеет читать explain plan и связывать его с observed runtime
- умеет объяснить, когда нужен broadcast, когда cache, когда repartition
- понимает базовые Spark config parameters и их последствия
- может сравнить baseline и tuned pipeline не на уровне ощущений, а на уровне артефактов и замеров

## Questions for review
- почему shuffle дорогой с точки зрения CPU, disk и network?
- как AQE меняет поведение Spark job?
- почему неправильная конфигурация может убить производительность даже при хорошем коде?

