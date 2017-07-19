# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure(2) do |config|
  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://atlas.hashicorp.com/search.
  config.vm.define "tdd" do |tdd|
      tdd.vm.box = "ubuntu/xenial64"
      # set up network ip and port forwarding
      tdd.vm.network "forwarded_port", guest: 5000, host: 5000, host_ip: "127.0.0.1"
      tdd.vm.network "private_network", ip: "192.168.33.10"

      # Windows users need to change the permissions explicitly so that Windows doesn't
      # set the execute bit on all of your files which messes with GitHub users on Mac and Linux
      tdd.vm.synced_folder "./", "/vagrant", owner: "ubuntu", mount_options: ["dmode=755,fmode=644"]

      tdd.vm.provider "virtualbox" do |vb|
        # Customize the amount of memory on the VM:
        vb.memory = "512"
        vb.cpus = 1
      end
  end

  # Copy your .gitconfig file so that your git credentials are correct
  if File.exists?(File.expand_path("~/.gitconfig"))
    config.vm.provision "file", source: "~/.gitconfig", destination: "~/.gitconfig"
  end

  # Copy your ssh keys for github so that your git credentials work
  if File.exists?(File.expand_path("~/.ssh/id_rsa"))
    config.vm.provision "file", source: "~/.ssh/id_rsa", destination: "~/.ssh/id_rsa"
  end

  # Enable provisioning with a shell script. Additional provisioners such as
  # Puppet, Chef, Ansible, Salt, and Docker are also available. Please see the
  # documentation for more information about their specific syntax and use.
  config.vm.provision "shell", inline: <<-SHELL
    apt-get update
    apt-get install -y git python-pip python-dev build-essential
    pip install --upgrade pip
    apt-get -y autoremove
    # Install app dependencies
    cd /vagrant
    sudo pip install -r requirements.txt
    # Make vi look nice
    sudo -H -u ubuntu echo "colorscheme desert" > ~/.vimrc
  SHELL

end
