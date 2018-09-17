"""
After moving all the files using the 1_ file, we run this one to extract
the images from the videos and also create a data file we can use
for training and testing later.
"""
import csv
import glob
import os
import os.path
from subprocess import call
import cv2


def dump_frames(vid_path, output):
    # Log the time
    # Start capturing the feed
    cap = cv2.VideoCapture(vid_path)
    # Find the number of frames
    video_length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) - 1
    print ("Number of frames: ", video_length)
    count = 0
    # Start converting the video
    while cap.isOpened():
        # Extract the frame
        ret, frame = cap.read()
        # Write the results back to output location.
        cv2.imwrite('{}-{:04d}.jpg'.format(output, count + 1),
                    frame, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
        count = count + 1
        # If there are no more frames left
        if (count > (video_length - 1)):
            # Log the time again
            # Release the feed
            cap.release()
            # Print stats
            break


def dump_frames2(vid_path, out_full_path):

    video = cv2.VideoCapture(vid_path)

    fcount = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    for i in range(fcount):
        ret, frame = video.read()
        assert ret
        cv2.imwrite('{}-{:04d}.jpg'.format(out_full_path, i),
                    frame, [int(cv2.IMWRITE_JPEG_QUALITY), 100])


def extract_files():
    """After we have all of our videos split between train and test, and
    all nested within folders representing their classes, we need to
    make a data file that we can reference when training our RNN(s).
    This will let us keep track of image sequences and other parts
    of the training process.

    We'll first need to extract images from each of the videos. We'll
    need to record the following data in the file:

    [train|test], class, filename, nb frames

    Extracting can be done with ffmpeg:
    `ffmpeg -i video.mpg image-%04d.jpg`
    """
    data_file = []
    folders = ['./train/', './test/', './validation/']

    for folder in folders:
        class_folders = glob.glob(folder + '*')
        for class_folder in class_folders:
            label_folders = glob.glob(class_folder + '/*')
            for vid_class in label_folders:
                class_files = glob.glob(vid_class + '/*.avi')

                for video_path in class_files:
                    # Get the parts of the file.
                    video_parts = get_video_parts(video_path)

                    train_or_test, classname, videofoldername, filename_no_ext, filename = video_parts

                    # Only extract if we haven't done it yet. Otherwise, just get
                    # the info.
                    if not check_already_extracted(video_parts):
                        # Now extract it.
                        src = train_or_test + '/' + classname + '/' + videofoldername + '/' +\
                            filename
                        # dest = train_or_test + '/' + classname + '/' + videofoldername + '/' +\
                        #     filename_no_ext + '-%04d.jpg'
                        dest = train_or_test + '/' + classname + '/' + videofoldername + '/' +\
                            filename_no_ext
                        # call(["ffmpeg", "-i", src, "-vcodec", "copy", dest])
                        dump_frames(src, dest)
                    # Now get how many frames it is.
                    nb_frames = get_nb_frames_for_video(video_parts)

                    data_file.append(
                        [train_or_test, classname, filename_no_ext, nb_frames])

                    print("Generated %d frames for %s" %
                          (nb_frames, filename_no_ext))

    with open('data_file.csv', 'w') as fout:
        writer = csv.writer(fout)
        writer.writerows(data_file)

    print("Extracted and wrote %d video files." % (len(data_file)))


def get_nb_frames_for_video(video_parts):
    """Given video parts of an (assumed) already extracted video, return
    the number of frames that were extracted."""
    train_or_test, classname, videofoldername, filename_no_ext, _ = video_parts
    generated_files = glob.glob(train_or_test + '/' + classname + '/' + videofoldername + '/' +
                                filename_no_ext + '*.jpg')
    return len(generated_files)


def get_video_parts(video_path):
    """Given a full path to a video, return its parts."""
    parts = video_path.split('/')
    filename = parts[4]
    filename_no_ext = filename.split('.')[0]
    videofoldername = parts[3]
    classname = parts[2]
    train_or_test = parts[1]

    return train_or_test, classname, videofoldername, filename_no_ext, filename


def check_already_extracted(video_parts):
    """Check to see if we created the -0001 frame of this file."""
    train_or_test, classname, videofoldername, filename_no_ext, _ = video_parts
    return bool(os.path.exists(train_or_test + '/' + classname + '/' + videofoldername +
                               '/' + filename_no_ext + '-0001.jpg'))


def main():
    """
    Extract images from videos and build a new file that we
    can use as our data input file. It can have format:

    [train|test], class, filename, nb frames
    """
    extract_files()


if __name__ == '__main__':
    main()
