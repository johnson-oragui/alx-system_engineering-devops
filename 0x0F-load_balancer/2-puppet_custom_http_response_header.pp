# Puppet manifest to configure Nginx and HAProxy
package { 'nginx':
  ensure => installed,
}

file { '/var/www/html':
  ensure => directory,
}

file { '/var/www/html/index.html':
  ensure  => present,
  content => 'Hello World!',
}

file { '/var/www/html/404.html':
  ensure  => present,
  content => 'Ceci n\'est pas une page',
}

file { '/etc/nginx/sites-available/default':
  ensure  => present,
  content => '
    server {
      listen 80 default_server;
      listen [::]:80 default_server;
      add_header X-Served-By $hostname;
      root /var/www/html;
      index index.html index.htm;

      rewrite ^/redirect_me$ http://google.com/ permanent;

      error_page 404 /404.html;
      location = /404.html {
        internal;
      }
    }
  ',
}

service { 'nginx':
  ensure  => running,
  enable  => true,
  require => File['/etc/nginx/sites-available/default'],
}
