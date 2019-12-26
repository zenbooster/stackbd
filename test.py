#!/usr/bin/python3
import os
import sys
import time
import hashlib

CC_DEV = '/dev/stackbd0'
MNT_POINT = '/mnt/'
SAMPLE_FOLDER = os.path.expanduser('/home/user/samples/')
SAMPLE_FILE_NAME = 'big'
#SAMPLE_FILE_NAME = '70m'
SAMPLE_FILE_SRC_1 = SAMPLE_FOLDER + SAMPLE_FILE_NAME
SAMPLE_FILE_DST_1 = MNT_POINT + SAMPLE_FILE_NAME
SAMPLE_FILE_SRC_2 = SAMPLE_FILE_DST_1
SAMPLE_FILE_DST_2 = SAMPLE_FILE_SRC_1 + '_2'
NUM_OF_EPOCHS = 1

def chk_ret(ret):
  if ret:
    print('err ({})'.format(ret))
    exit(ret)
  else:
    print('ok')

def mount_cc():
  print ('монтируем криптоконтейнер...', end='')
  sys.stdout.flush()
  ret = os.system('mount {} {}'.format(CC_DEV, MNT_POINT));
  chk_ret(ret)

def umount_cc():
  print ('отмонтируем криптоконтейнер...', end='')
  sys.stdout.flush()
  ret = os.system('umount {}'.format(MNT_POINT));
  chk_ret(ret)

def benchmark(func):
  def wrapper(*args, **kwargs):
    start = time.time()
    ret = func(*args, **kwargs)
    sec = time.time() - start
    print('%s: [%d сек.; %.1f мб/сек.]' % (func.__name__, sec, sec and 500.0 / sec or 0))
    return ret
  return wrapper

@benchmark
def copy_to_cc():
  print ('копируем образец в криптоконтейнер...', end='')
  sys.stdout.flush()
  ret = os.system('rsync --progress {} {}'.format(SAMPLE_FILE_SRC_1, SAMPLE_FILE_DST_1));
  chk_ret(ret)
  print ('sync...', end='')
  sys.stdout.flush()
  ret = os.system('sync {}'.format(SAMPLE_FILE_DST_1));
  chk_ret(ret)

@benchmark
def copy_from_cc():
  print ('копируем образец из криптоконтейнера...', end='')
  sys.stdout.flush()
  ret = os.system('rsync --progress {} {}'.format(SAMPLE_FILE_SRC_2, SAMPLE_FILE_DST_2));
  chk_ret(ret)

def del_file(name):
    ret = os.path.isfile(name)
    if ret:
      try:
        print('удаляем <{}>... '.format(name), end='')
        sys.stdout.flush()
        os.remove(name)
        print('ok')

      except (OSError, e):
        chk_ret(e.errno)

    return ret

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

################
print('Скрипт тестирующий AldCC')
ret = 0

for i in range(0, NUM_OF_EPOCHS):
  print('Эпоха #{}'.format(i))
  mount_cc()
  copy_to_cc()
  umount_cc()

  mount_cc()
  copy_from_cc()

  print('Проверка хэшей...', end='')
  sys.stdout.flush()
  md0 = md5(SAMPLE_FILE_SRC_1)
  md1 = md5(SAMPLE_FILE_DST_2)
  ret = md0 != md1
  if ret:
    print('err')
  else:
    print('ok')

  del_file(SAMPLE_FILE_DST_1)
  umount_cc()
  del_file(SAMPLE_FILE_DST_2)

  if ret:
    break

  print('================')


exit(ret)
