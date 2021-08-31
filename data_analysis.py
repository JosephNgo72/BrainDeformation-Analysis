from os import listdir
from os.path import isfile, join
import h5py
import time

DIR_DATA_XYZ_MPS = 'C:/Users/josep/OneDrive/Desktop/Camarillo/Maximum Principal Strain/XYZ_mps'
DIR_DATA_XNYZ_MPS = 'C:/Users/josep/OneDrive/Desktop/Camarillo/Maximum Principal Strain/XNYZ_mps'


def main():
    start_time = time.time()
    f = h5py.File('mps_dataset.hdf5', 'r')

    datasetXYZ_names = [f for f in listdir(DIR_DATA_XYZ_MPS) if isfile(join(DIR_DATA_XYZ_MPS, f))]
    datasetXNYZ_names = [f for f in listdir(DIR_DATA_XNYZ_MPS) if isfile(join(DIR_DATA_XNYZ_MPS, f))]

    impact_id = 1
    impacts_net_deformations = []
    for dsname in datasetXYZ_names:
        dsloc = 'XYZ_MPS/' + dsname
        dataset = f[dsloc]

        # for each impact
        data_entries = []
        for i in range(len(dataset)):
            # for every row(time interval), get the first brain element's measure of deformation
            data_entries.append(dataset[i][0])

        print('Brain Impact Number #', impact_id)
        impact_id += 1

        min_brain_deformation = min(data_entries)
        print('Minimum:', min_brain_deformation)

        max_brain_deformation = max(data_entries)
        print('Maximum:', max_brain_deformation)

        net_brain_deformation = max_brain_deformation - min_brain_deformation
        impacts_net_deformations.append(net_brain_deformation)
        print('Net Brain Deformation:', net_brain_deformation)
        num_sec = time.time() - start_time
        print('Time Elapsed: ' + str(int(num_sec // 60)) + 'min ' + str("{:.2f}".format(num_sec % 60)) + 'sec')
        print()
    for dsname in datasetXNYZ_names:
        dsloc = 'XNYZ_MPS/' + dsname
        dataset = f[dsloc]

        # for each impact
        data_entries = []
        for i in range(len(dataset)):
            # for every row(time interval), get the first brain element's measure of deformation
            data_entries.append(dataset[i][0])

        print('Brain Impact Number #', impact_id)
        impact_id += 1

        min_brain_deformation = min(data_entries)
        print('Minimum:', min_brain_deformation)

        max_brain_deformation = max(data_entries)
        print('Maximum:', max_brain_deformation)

        net_brain_deformation = max_brain_deformation - min_brain_deformation
        impacts_net_deformations.append(net_brain_deformation)
        print('Net Brain Deformation:', net_brain_deformation)
        num_sec = time.time() - start_time
        print('Time Elapsed: ' + str(int(num_sec // 60)) + 'min ' + str("{:.2f}".format(num_sec % 60)) + 'sec')
        print()

    print('Highest Brain Deformation: ' + str(max(impacts_net_deformations)) + " on impact #" + str(impacts_net_deformations.index(max(impacts_net_deformations))+1))
    print('Lowest Brain Deformation: ' + str(min(impacts_net_deformations)) + " on impact #" + str(impacts_net_deformations.index(min(impacts_net_deformations))+1))

    average_brain_deformation = sum(impacts_net_deformations)/len(impacts_net_deformations)
    print('Average Brain Deformation across 1065 impacts:', average_brain_deformation)

    impacts_net_deformations.sort()
    median_brain_deformation = impacts_net_deformations[len(impacts_net_deformations)//2]
    print('Median Brain Deformation across 1065 impacts:', median_brain_deformation)

    num_sec = time.time() - start_time
    print('Total time of analysis: ' + str(int(num_sec // 60)) + 'min ' + str("{:.2f}".format(num_sec % 60)) + 'sec')
    print('Analysis Complete')


if __name__ == '__main__':
    main()
