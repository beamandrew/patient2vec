## Load the requirements ##
import csv
import random
from annoy import AnnoyIndex


def build_index(df,n_trees = 50,dist_metric='angular',out_dir="./"):
    n_records = df.shape[0]
    n_col = df.shape[1]
    index = AnnoyIndex(n_col,metric=dist_metric)
    patient_dict = {}
    index_dict = {}
    i = 0
    print "Adding items to the index..."
    for patient_id in df.index.values:
        if i % 10000 == 0:
            print str(i)
        vec = df.loc[patient_id].values
        index.add_item(i,vec)
        patient_dict[patient_id] = i
        index_dict[i] = patient_id
        i += 1
    print "Building the index..."
    index.build(n_trees)
    index.save(out_dir+"annoy_index.ann")
    ## Save the patient_id -> index mapping ##
    w = csv.writer(open(out_dir+"patient_mapping.csv", "w"))
    for key, val in patient_dict.items():
        w.writerow([key, val])
    w = csv.writer(open(out_dir+"index_mapping.csv", "w"))
    for key, val in index_dict.items():
        w.writerow([key, val])

def generate_sentence(start,neighbor_dict,n_neighbors,walk_size):
    sentence = str(start)
    current_patient = start
    for i in (range(walk_size-1)):
        neighbors = neighbor_dict[current_patient]
        next_patient = random.sample(neighbors, 1)[0]
        sentence += " " + next_patient
        current_patient = next_patient
    return sentence


def create_walks(df,index_file,patient_dict_file,index_dict_file,n_neighbors = 25,walks_per_patient=10,walk_size=50,out_dir="./"):
    index = AnnoyIndex(df.shape[1])
    index.load(index_file)
    patient_dict = {}
    for key, val in csv.reader(open(patient_dict_file)):
        patient_dict[key] = int(val)
    index_dict = {}
    for key, val in csv.reader(open(index_dict_file)):
        index_dict[int(key)] = val
    print("Computing nearest-neighbors...")
    neighbor_dict = {}
    for i in range(index.get_n_items()):
        if i % 1000 == 0:
            print str(i)
        patient_id = index_dict[i]
        neighbors = index.get_nns_by_item(i=i, n=n_neighbors, search_k=-1, include_distances=False)
        neighbor_ids = [index_dict[x] for x in neighbors]
        neighbor_dict[patient_id] = neighbor_ids
    f = open(out_dir+"patient_walks.txt", 'wb')
    for i in range(index.get_n_items()):
        if i % 1000 == 0:
            print str(i)
        patient_id = index_dict[i]
        patient_sentences = ""
        for j in range(walks_per_patient):
            sentence = generate_sentence(start=patient_id,neighbor_dict=neighbor_dict,
                                        n_neighbors=n_neighbors,walk_size=walk_size)
            patient_sentences = sentence + "\n"
            ## Write it ##
        f.write(patient_sentences)
