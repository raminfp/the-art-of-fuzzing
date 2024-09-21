### GitLab Fuzzing-CI/CD


# Download and install the binary for your system
```bash
$ sudo curl -L --output /usr/local/bin/gitlab-runner https://gitlab-runner-downloads.s3.amazonaws.com/latest/binaries/gitlab-runner-linux-amd64
```
# Give it permissions to execute
```bash
$ sudo chmod +x /usr/local/bin/gitlab-runner
```

# Create a GitLab CI user
```bash
$ sudo useradd --comment 'GitLab Runner' --create-home gitlab-runner --shell /bin/bash
```
# Install and run as service
```bash
$ sudo gitlab-runner install --user=gitlab-runner --working-directory=/home/gitlab-runner
$ sudo gitlab-runner start
$ gitlab-runner register
```

# Fix issue (Shell executor fails to prepare environment)

```bash
$ nano /home/gitlab-runner/.bash_logout 

# ~/.bash_logout: executed by bash(1) when login shell exits.

# when leaving the console clear the screen to increase privacy

#if [ "$SHLVL" = 1 ]; then
#    [ -x /usr/bin/clear_console ] && /usr/bin/clear_console -q
#fi



```