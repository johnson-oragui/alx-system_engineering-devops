#!/usr/bin/env bash
# Using puppet to connect without password

package { 'augeas-tools':
  ensure => installed,
}

augeas { 'Turn off passwd auth':
  context => '/files/etc/ssh/sshd_config',
  changes => [
    'set #comment[.="*PasswordAuthentication*"]/../PasswordAuthentication no',
  ],
}

augeas { 'Declare identity file':
  context => '/files/etc/ssh/ssh_config',
  changes => [
    'set #comment[.="*IdentityFile*"]/../IdentityFile ~/.ssh/school',
  ],
}
