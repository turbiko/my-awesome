https://www.inmotionhosting.com/support/server/linux/create-sudo-user-ubuntu-20
sudo <command>

## Add a Sudo User

ssh root@example.com

adduser <user>

Finally, add the new user to the “sudo” group by running this command:
```bash
usermod -aG sudo <user>
```

```bash
su <user>
```


## How to Log In With SSH Key

Whil still logged in as the sudo user, edit the SSH configuration file:

```bash
sudo nano /etc/ssh/sshd_config
```

AllowGroups wheel root

```bash
==- PermitRootLogin without-password==
==+ PermitRootLogin no==
```

cd .ssh

```bash
nano authorized_keys
```

```bash
chmod 600 authorized_keys
```

```bash
chmod 700 .ssh
```

```bash
sudo service ssh restart
```

```bash
ssh <user>@example.com
```

