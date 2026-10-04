# Important functions (grouped)

## Command execution

- `run_command`
- `sh`
- `get_error_code`
- `get_last_error`

## Working directory

- `cwd`
- `current_dir`
- `get_current_dir`
- `cd`
- `chdir`
- `set_current_dir`

## Find / list files

- `find`
- `find_dir`
- `check_ext`
- `get_filename`

## Read / write file content

- `get_file_content`
- `save_file_content`
- `tail`

## Copy / move / remove files and directories

- `cp`
- `copy_file`
- `copy_files`
- `copy_file_with_progress`
- `mv`
- `rm`
- `rmdir`
- `touch`
- `chmod`
- `chown`

## File times (timestamps)

- `get_file_write_time`
- `set_file_write_time`
- `get_file_create_time`
- `set_file_create_time`

## Process helpers

- `proc_present`
- `get_proc_list`
- `proc_list_to_dict`
- `proc_list_to_pid_list`
- `proc_list_to_names_list`

## Datetime helpers

- `now`
- `get_datetime`
- `delay`
- `datetime_parse`
- `datetime_to_str`
- `datetime_to_yyyy_mm_dd_hh_mm_ss`
- `datetime_to_yyyy_mm_dd_hh_mm`
- `datetime_to_yyyy_mm_dd`
- `datetime_to_hh_mm_ss`
- `datetime_to_hh_mm`
- `datetime_trim_ms`
- `datetime_trim_second`
- `datetime_trim_time`

## File lists (batch helpers)

- `file_list_calc_total_size`
- `file_list_filter_by_flags`
- `file_list_filter_by_substring`
- `file_list_sort_by_date`
- `file_list_sort_by_size`
- `file_list_sort_by_name`
- `file_list_sort_by_ext`

## Config helpers

- `load_config_from_yaml`
- `load_config_from_ini`
- `load_config_from_json`

## yaml

- `load_from_yaml`
- `save_to_yaml`

## Misc

- `format_bytes`
- `contains_path_glob_pattern`
