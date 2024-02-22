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

## Resizing Root Filesystem

By default, buildroot will generate an image with a root filesystem of only **268 MB**, this can be a problem for people wanting to import large datasets.

```text
Number  Start   End     Size    Type     File system  Flags
 1      1049kB  67.1MB  66.1MB  primary  fat16        boot, lba
 2      68.2MB  337MB   268MB   primary  ext4
```

To expand the filesystem after flashing you must first expand the partition, and then the filesystem itself.

`resize2fs` **requires the partition device and not the regular device.** For example, `/dev/sdb2` instead of if `/dev/sdb` was the SD card device for the second partition.

```bash
# Unmount all mounted partitions on device
sudo umount /dev/something*

# Resize root filesystem partition to 100% of remaining space on SD card
sudo parted -s /dev/something resizepart 2 100%

# Check and resize ext4 filesystem to fill new space
sudo e2fsck -f /dev/something2
sudo resize2fs /dev/something2
```

### (Ubuntu 22.04 Host) Outdated e2fsprogs

Buildroot appears to create the ext4 filesystem with a newer version of e2fsprogs than what Ubuntu has in the 22.04 repository, leading to this message:

```text
resize2fs 1.46.5 (30-Dec-2021)                                                                                                                                                               
resize2fs: Filesystem has unsupported feature(s) (/dev/sdc2)
```

The fastest way around this is to leverage docker like so (remember to replace `/dev/something2`):

```bash
docker run -it --rm --privileged -v /dev/something2:/disk ubuntu:rolling \
bash -c "e2fsck -f /disk && resize2fs /disk"
```
