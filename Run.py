import cv2
import numpy as np
# ---------- Source Files --------#
import Image_Preparation as img
import Data_Embedding as stego


NUM_CHANNELS = 3
COVER_IMAGE_FILEPATH = " " 
STEGO_IMAGE_FILEPATH = "./stego_image.jpg"
SECRET_MESSAGE_STRING = "A"

#====================================================================================================#
#====================================================================================================#

cover_image = cv2.imread(COVER_IMAGE_FILEPATH, flags=cv2.IMREAD_COLOR)
height, width = cover_image.shape[:2]
# Image Dimensions to be 8x8
while (height % 8):
    height += 1  # Rows
while (width % 8):
    width += 1  # Cols
valid_dim = (width, height)
padded_image = cv2.resize(cover_image, valid_dim)
cover_image_f32 = np.float32(padded_image)
#RGB
cover_image_YCC = img.YCC_Image(
    cv2.cvtColor(cover_image_f32, cv2.COLOR_BGR2YCrCb))

# holding stego image data in empty nd.array
stego_image = np.empty_like(cover_image_f32)

#====================================================================================================#
#====================================================================================================#

for chan_index in range(NUM_CHANNELS):
    # DCT 
    dct_blocks = [cv2.dct(block)
                  for block in cover_image_YCC.channels[chan_index]]

    # QUANTIZATION 
    dct_quants = [np.around(np.divide(item, img.JPEG_STD_LUM_QUANT_TABLE))
                  for item in dct_blocks]
    # Embed data 
    if (chan_index == 0):
        
        dct_quants = stego.embed_encoded_data_into_DCT2(dct_quants,SECRET_MESSAGE_STRING)
    


    # DEQUANTIZATION 
    dct_dequants = [np.multiply(data, img.JPEG_STD_LUM_QUANT_TABLE)
                    for data in dct_quants]

    # IDCT
    idct_blocks = [cv2.idct(block) for block in dct_dequants]

    # Rebuild full image channel
    stego_image[:, :, chan_index] = np.asarray(
        img.stitch_8x8_blocks_back_together(cover_image_YCC.width, idct_blocks))

#====================================================================================================#
#====================================================================================================#

# Convert back to RGB
stego_image_RGB = cv2.cvtColor(stego_image, cv2.COLOR_YCR_CB2BGR)

# Pixel Values to [0 - 255]
final_stego_image = np.uint8(np.clip(stego_image_RGB, 0, 255))

# Save Stego image
cv2.imwrite(STEGO_IMAGE_FILEPATH, final_stego_image)