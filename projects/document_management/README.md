Goals:   A toolset to  keep, organize, backup important files


Workflow:     Once you get a important file 

1. You put it (im_file) into a raw_files directory
2. The file will be hashed, the tool will check whether the file is in database according to hash number. 
   1. get_hash(file) ,  check_file_in_db(hash), 
3. If the file is in database, we move the file to processed directory,  im_file and a symlink of the backuped file im_file_bak.lnk was created for user to double check they are the same. 
   1. wait_for_check(file) get_backuped_file(hash)
4. If the file is not in database, we create an hard link in backuped_files/hashed_files.  Another hard link in backuped_files/to_be_organized.  The file could be rename and moved to any backuped_files/file_layout_type. 
   1. cp -al dirA dirB  copy whole directory as hard link
   2. The backuped_files/hashed_files is organized by two layers of directories.  The first layer is the first two bytes of hash number, the second layer is the third and forth bytes of hash number.
   3. The files in backuped_files/hashed_files need special function to remove.  
      1. anihinate_hash(hash) 
      2. relink_layout(directory) - make sure all  backuped_files/file_layout_type files are hard link of  backuped_files/hashed_files
5. You will always backup the whole backuped_files/ directory buy hard links on the same hard drive, and make regular backups on other hard drivers.  
6. The hash database file should be kept through git.
