# Kills a process named killmenow

# Define the exec resource to kill the process
exec { 'kill_killmenow_process':
  command => 'pkill -f killmenow',
  path    => '/usr/bin:/bin',
  onlyif  => 'pgrep -f killmenow',
}
