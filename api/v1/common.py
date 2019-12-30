
diris_spool_dir="/run/diris/"

def read_counter(counter):
    # Read Diris counter value stored in file

    try:
        counter_file=open(diris_spool_dir + str(counter), 'r')
        counter_data = counter_file.read()
        counter_file.close()
        return counter_data
    except:
        return None

