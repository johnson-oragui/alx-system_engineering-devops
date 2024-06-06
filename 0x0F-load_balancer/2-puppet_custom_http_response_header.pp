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

package { 'haproxy':
  ensure => installed,
}

file { '/etc/haproxy/haproxy.cfg':
  ensure  => present,
  content => '
    global
      log /dev/log local0
      chroot /var/lib/haproxy
      user haproxy
      group haproxy
      daemon

    defaults
      mode http
      log global
      option httplog
      option dontlognull
      option redispatch
      retries 3
      timeout http-request 10s
      timeout queue 1m
      timeout connect 10s
      timeout client 1m
      timeout server 1m
      timeout http-keep-alive 10s
      timeout check 10s

    frontend http_front
      bind *:80
      default_backend Jtechofficial_tech_backend

    backend Jtechofficial_tech_backend
      balance roundrobin
      server server1 54.87.224.2:80 check
      server server2 54.89.109.20:80 check
  ',
}

service { 'haproxy':
  ensure  => running,
  enable  => true,
  require => File['/etc/haproxy/haproxy.cfg'],
}
