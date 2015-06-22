#
# Cookbook Name:: junos-config
# Recipe:: setup_host
#
# Prepare the Linux host to run script to push config changes.
#
# Copyright (C) 2015 Arne Sund
#


case node["platform_family"]
when "debian"
    include_recipe 'apt'
end


# Install necessary packages for the chosen platform (debian/rhel/etc.)
node["junos-config"]["packages"][node["platform_family"]].each do |package_name|
    package package_name do
        action :install
    end
end

# Install Juniper PyEZ library
python_pip "junos-eznc"

