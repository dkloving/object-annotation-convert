from pathlib import PurePath


def describe_folders(file_list):
    from collections import Counter
    """ TODO: move this outside of class to a utils module """
    folder_counts = Counter([PurePath(file).parent for file in set(file_list)])
    output_string = 'File counts per folder:\n'
    for folder in folder_counts:
        output_string += '\t{}:\t{}\n'.format(folder, folder_counts[folder])
    output_string += 'Total files: {}'.format(len(set(file_list)))
    return output_string
