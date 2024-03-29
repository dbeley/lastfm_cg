import numpy as np
from PIL import Image
from io import BytesIO
import logging

logger = logging.getLogger(__name__)
logging.getLogger("PIL").setLevel(logging.WARNING)
logging.getLogger("numpy").setLevel(logging.WARNING)


def chunks(l, n):
    # generator of chunks of size l for a iterable n
    for i in range(0, len(l), n):
        yield l[i : i + n]


def create_image(list_covers, nb_columns):
    # create image from list_covers with nb_columns columns
    imgs = [Image.open(BytesIO(i)).convert("RGB") for i in list_covers]

    min_shape = sorted([(np.sum(i.size), i.size) for i in imgs])[0][1]

    logger.info("Creating image.")
    logger.debug(
        "Image : %s columns, %s covers. min_shape : %s.",
        nb_columns,
        len(list_covers),
        min_shape,
    )
    list_comb = []
    for img in chunks(imgs, nb_columns):
        # list of rows of x columns
        list_arrays = [np.asarray(i.resize(min_shape)) for i in img]
        i = 0
        while len(list_arrays) < nb_columns:
            i += 1
            logger.debug("Missing album cover. Creating empty square %s.", i)
            list_arrays.append(
                np.asarray(np.zeros((min_shape[0], min_shape[1], 4), dtype=np.uint8))
            )
        logger.debug("len list_arrays : %s.", len(list_arrays))
        list_comb.append(np.hstack(list_arrays))

    # combine rows to create image
    list_comb_arrays = [np.asarray(i) for i in list_comb]
    imgs_comb = np.vstack(list_comb_arrays)
    imgs_comb = Image.fromarray(imgs_comb)
    return imgs_comb


def create_top100_image(list_covers):
    # for now the number of column on each row must be a multiple of the first element to work properly
    list_columns = [5, 5, 10, 10, 10, 15, 15, 15, 15]
    imgs = [Image.open(BytesIO(i)).convert("RGB") for i in list_covers]

    min_shape = sorted([(np.sum(i.size), i.size) for i in imgs])[0][1]

    logger.info("Creating image.")
    logger.debug(
        "Image : %s columns, 100 covers. min_shape : %s.",
        len(list_covers),
        min_shape,
    )

    list_comb = []
    i = 0
    chunks = []

    for chunksize in list_columns:
        chunks.append(imgs[i : i + chunksize])
        i += chunksize

    for row in chunks:
        shape = (int(min_shape[0] / (len(row) / 5)), int(min_shape[1] / (len(row) / 5)))
        list_arrays = [np.asarray(i.resize(shape)) for i in row]
        list_comb.append(np.hstack(list_arrays))

    # combine rows to create image
    list_comb_arrays = [np.asarray(i) for i in list_comb]
    imgs_comb = np.vstack(list_comb_arrays)
    imgs_comb = Image.fromarray(imgs_comb)
    return imgs_comb
