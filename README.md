# hammer-scripts

### Deploying RHV on fusor-dev
1. ssh into fusor-dev `vagrant ssh`
2. `cd /projects/hammer-scripts`
2. `./prepare-org.sh`
3. `./manage-content.sh` and wait for sync to complete.  Retry if necessary.  TODO: Poll foreman task status and complete task when all tasks are successful.
4. `./configure_host_groups.py`


### Known issues
* prepare-org.sh
  *  does not replicate fusor task ImportAccessInsights since it's done using PuppetClassImporter instead of an api or hammer command.  Requires more research.
