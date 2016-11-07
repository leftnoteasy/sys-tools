# Usage:
# python ....py directory original_symbolic_target_prefix new_symbolic_target_prefix

import os
import os.path
import fnmatch
import sys
import errno

def symlink_force(target, link_name):
    try:
        os.symlink(target, link_name)
    except OSError, e:
        if e.errno == errno.EEXIST:
            os.remove(link_name)
            os.symlink(target, link_name)
        else:
            raise e

if __name__ == "__main__":
  folder = sys.argv[1]
  original_sym_prefix = os.path.realpath(sys.argv[2])
  new_sym_prefix = os.path.realpath(sys.argv[3])

  for root, dirnames, filenames in os.walk(folder):
    
    for filename in filenames:
       filename = os.path.join(root, filename)
       print "Looking at file:" + filename

       if os.path.islink(filename):
         print "looking at link: ", filename

         original_target_path = os.path.realpath(os.readlink(filename))
         if original_target_path.startswith(original_sym_prefix):
            new_target_path = os.path.join(new_sym_prefix, os.path.relpath(original_target_path, original_sym_prefix))
            symlink_force(new_target_path, filename)

            print "-- relink link from:" + original_target_path + " to:" + new_target_path
            

