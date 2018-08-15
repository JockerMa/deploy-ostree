# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "bento/debian-9"

  config.vm.provider "virtualbox" do |vb|
    vb.memory = "1024"
    vb.cpus = 2
  end

  config.vm.provision :docker
  config.vm.provision :shell, inline: <<-EOF
    apt-get update
    apt-get install -y python3 python3-pip
    pip3 install /vagrant[dev]
    echo cd /vagrant >> ~vagrant/.profile
  EOF
end
