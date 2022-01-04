#/bin/bash
read -p "Please enter your username: " username
read -sp "Please enter your password: " SSHPASS

declare -a devices=(
"10.10.0.1"
"10.10.0.130"
)
echo ""
for dev in ${devices[@]}; do
   echo "Logging into device $dev"
   version=`sshpass -p "$SSHPASS" ssh -o StrictHostKeyChecking=no $username@$dev "show version"`
   echo "$version"
done
