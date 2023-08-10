# Using puppet to find out why Apache is returning a 500 error.

# Define an exec resource to restart Apache after applying the fix
exec { 'restart_apache':
  command     => '/usr/sbin/service apache2 restart',
  refreshonly => true,
}

# Define a file resource to update the Apache configuration file
file { '/etc/apache2/sites-available/000-default.conf':
  ensure  => file,
  content => template('apache/000-default.conf.erb'),
  require => Exec['restart_apache'],
}

# Define an Apache vhost template (apache/000-default.conf.erb)
file { '/etc/apache2/sites-available/000-default.conf':
  ensure => file,
  source => 'puppet:///modules/apache/000-default.conf',
}

# Define a service resource to ensure Apache is running
service { 'apache2':
  ensure => running,
}
