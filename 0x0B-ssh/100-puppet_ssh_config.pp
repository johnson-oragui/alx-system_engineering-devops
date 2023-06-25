#!/usr/bin/env bash
# Using puppet to connect without password

file_line { 'Turn off passwd auth':
  path  => '/etc/ssh/sshd_config',
  line  => 'PasswordAuthentication no',
}

file_line { 'Declare identity file':
  path  => '/etc/ssh/ssh_config',
  line  => 'IdentityFile ~/.ssh/school',
}

service { 'ssh':
  ensure => 'running',
  enable => true,
}
