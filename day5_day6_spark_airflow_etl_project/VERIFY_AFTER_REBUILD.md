# Verify Java/Spark fix

Run from this folder:

```bash
chmod +x rebuild_day56_clean.sh
./rebuild_day56_clean.sh
```

Expected inside `day56-airflow-scheduler`:

```text
openjdk version ...
JAVA_HOME=/usr/lib/jvm/default-java
/usr/lib/jvm/default-java/bin/java
ps from procps-ng ...
```

If the Airflow task log still shows:

```text
ps: command not found
/usr/lib/jvm/java-17-openjdk-arm64/bin/java: No such file or directory
```

then you are still running an old container or running Docker Compose from a different project folder.
