#! /bin/bash

# Compiles your dotnet project for Windows, Mac and Linux + x64/arm64 architecture 
# Put this script into project root (next to .sln)

NAME="RSS"
PUBLISHED="$PWD/published"

if [ -d "$PUBLISHED" ]; then
  rm -r "$PUBLISHED"
fi

function publish {
  dotnet publish -r "$1" --self-contained true -c Release -p:PublishSingleFile=true -p:EnableCompressionInSingleFile=true -p:IncludeNativeLibrariesForSelfExtract=true -o "$PUBLISHED"
  mv "$PUBLISHED/$NAME$2" "$PUBLISHED/$NAME_$1$2"
}

publish "win-x64" ".exe"
publish "linux-x64" ""
publish "osx-x64" ""
publish "win-arm64" ".exe"
publish "linux-arm64" ""
publish "osx-arm64" ""

rm "$PUBLISHED/$NAME.pdb"

