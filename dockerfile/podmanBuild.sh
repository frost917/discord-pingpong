#!/bin/bash

gitDir=$(dirname $(realpath $0))
serviceName="discord-pingpong"
imageTag="0.5"
manifestName="$REGISTRY/$serviceName:$imageTag"

# mount podman
mount -v /dev/zvol/data/buildah $dataRoot

# delete image manifest
podman --root $dataRoot image rm $manifestName

# create image manifest
podman --root $dataRoot manifest create $manifestName

# build images
for arch in amd64 arm64/v8
do 
	echo build $arch
	tag="$REGISTRY/$serviceName-$arch:$imageTag"
	echo $tag
	buildah bud \
		--root $dataRoot \
		--jobs=6 \
		--tag $tag \
		--platform linux/$arch \
		./

	result=`echo $?`
	if [[ $result != "0" ]]
		then
			echo "error occoured!"
			exit $result 
	fi

	echo add new image in manifeset
	podman --root $dataRoot manifest add $manifestName containers-storage:$tag
done

# push manifest
echo ==============================================
echo push $manifestName
podman --root $dataRoot manifest push --all --rm $manifestName docker://$manifestName
result=`echo $?`
echo $result
counter=0

while true;
do
	if [[ $result != "0" ]];
	then
		echo =============== UPLOAD RETRY ===================
		podman --root $dataRoot manifest push --all --rm $manifestName docker://$manifestName
		result=`echo $?`

		if [[ $counter -eq 3 ]];
		then
			exit 255
		fi

		counter=1+$counter
	else
		echo "upload complete!"
		echo ==============================================
		break
	fi
done
