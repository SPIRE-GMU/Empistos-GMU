# OP-TEE + DarknetZ Docker Build

## Introduction

This docker file runs a full standard rpi3 build of OP-TEE, including the [Darknetz example binary](https://github.com/mofanv/darknetz) as well as the [accompanying datasets.](https://github.com/mofanv/tz_datasets) in the root filesystem.

It also applies a number of patches to both OP-TEE and Darknetz to allow running on a Rasberry Pi 3B+ without error. These are visible in the patches directory.

## Quick Start

```bash
# Build the image from this folder
docker build -t optee:rpi3 .

# Run the image to generate files to be flashed to the SD card
docker run -it -v $PWD/out:/optee/out -v cache:/optee optee:rpi3
```

This will create an `out` folder in your current directory which will be populated with the image to be flashed to an SD card (`rpi3-sdcard.img`) along with some other files.

This will also create a docker volume called `cache` to speed up subsequent builds, currently it holds the entirety of the optee build folders so it can be quite large. You can delete it by running `docker volume rm cache`

If you do not care about building from scratch every single time, you can simply omit the `-v cache:/optee` from the run command above.

By default, make will run with 1 job process. For some reason when OP-TEE is built with more than one process, [the resulting image simply doesn't work.](https://github.com/OP-TEE/optee_os/issues/6284#issuecomment-1758781141) You can manually set the number of processes my adding `-e NPROC=1` to the docker run command where 1 is the number of processes

## Flashing

To flash the image to an SD card, you should **first make sure you have the right device file for it.** `dd` will not hesitate to destroy your computer's hard drive if you use it for the `of=` field. Use the command below (and some common sense) to make sure you know which device is your SD card. The easiest way to tell is usually by size.

```bash
lsblk -de7 -o PATH,SIZE,TRAN,MODEL,VENDOR
```

Once you are ready, run the below command to begin the flashing process. Replace `/dev/something` with your SD card's block device.

```bash
sudo dd if=./out/rpi3-sdcard.img of=/dev/something bs=1024k conv=fsync status=progress
```
