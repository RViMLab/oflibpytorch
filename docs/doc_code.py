import numpy as np
import cv2
import torch
import sys
sys.path.append('..')
import src.oflibpytorch as of
from src.oflibpytorch.utils import to_numpy, to_tensor, show_masked_image, unset_pure_pytorch, set_pure_pytorch


# # # # Usage / Visualisation
# shape = (601, 601)
# flow = of.Flow.from_transforms([['rotation', 601, 601, -30]], shape)
# flow_def = of.visualise_definition('bgr', return_tensor=False)
# cv2.imwrite('C:/Users/RVIM_Claudio/Downloads/usage_vis_flow.png', flow.visualise('bgr', return_tensor=False))
# cv2.imwrite('C:/Users/RVIM_Claudio/Downloads/usage_vis_flow_arrows.png',
#             flow.visualise_arrows(80, return_tensor=False))
# cv2.imwrite('C:/Users/RVIM_Claudio/Downloads/usage_vis_flow_definition.png', flow_def)
#
# mask = np.ones((601, 601), 'bool')
# mask[:301, :301] = False
# flow = of.Flow.from_transforms([['rotation', 601, 601, -30]], shape, mask=mask)
# cv2.imwrite('C:/Users/RVIM_Claudio/Downloads/usage_vis_flow_masked.png',
#             flow.visualise('bgr', True, True, return_tensor=False))
# cv2.imwrite('C:/Users/RVIM_Claudio/Downloads/usage_vis_flow_arrows_masked.png',
#             flow.visualise_arrows(80, show_mask=True, show_mask_borders=True, return_tensor=False))


# # # # Usage / Ref
# # Define a flow
# flow = of.Flow.from_transforms([['rotation', 200, 150, -30]], (300, 300), 't')
#
# # Get the flow inverse: in the wrong way, and correctly in either reference
# flow_invalid_inverse = -flow
# flow_valid_inverse_t = flow.invert('t')
# flow_valid_inverse_s = flow.invert('s')
# cv2.imwrite('C:/Users/RVIM_Claudio/Downloads/usage_ref_flow.png',
#             flow.visualise_arrows(30, show_mask=True, show_mask_borders=True, return_tensor=False))
# cv2.imwrite('C:/Users/RVIM_Claudio/Downloads/usage_ref_flow_inverse_wrong.png',
#             flow_invalid_inverse.visualise_arrows(30, show_mask=True, show_mask_borders=True, return_tensor=False))
# cv2.imwrite('C:/Users/RVIM_Claudio/Downloads/usage_ref_flow_inverse_t.png',
#             flow_valid_inverse_t.visualise_arrows(30, show_mask=True, show_mask_borders=True, return_tensor=False))
# cv2.imwrite('C:/Users/RVIM_Claudio/Downloads/usage_ref_flow_inverse_s.png',
#             flow_valid_inverse_s.visualise_arrows(30, show_mask=True, show_mask_borders=True, return_tensor=False))


# # # # Usage / Mask
# shape = (300, 400)
# flow_1 = of.Flow.from_transforms([['rotation', 200, 150, -30]], shape)
# flow_2 = of.Flow.from_transforms([['scaling', 100, 50, 0.7]], shape)
# result = flow_1.combine_with(flow_2, mode=3)
# cv2.imwrite('C:/Users/RVIM_Claudio/Downloads/usage_mask_flow1.png',
#             flow_1.visualise('bgr', return_tensor=False))
# cv2.imwrite('C:/Users/RVIM_Claudio/Downloads/usage_mask_flow2.png',
#             flow_2.visualise('bgr', return_tensor=False))
# cv2.imwrite('C:/Users/RVIM_Claudio/Downloads/usage_mask_result.png',
#             result.visualise('bgr', return_tensor=False))
# cv2.imwrite('C:/Users/RVIM_Claudio/Downloads/usage_mask_result_masked.png',
#             result.visualise('bgr', True, True, return_tensor=False))


# # # # Usage / Apply
# img = cv2.imread('_static/thames_300x400.jpg')
# transforms = [['rotation', 200, 150, -30], ['scaling', 100, 50, 0.7]]
# flow = of.Flow.from_transforms(transforms, img.shape[:2])
# warped_img, valid_area = flow.apply(to_tensor(img, True), return_valid_area=True)
# cv2.imwrite('C:/Users/RVIM_Claudio/Downloads/usage_apply_thames_warped1.png',
#             show_masked_image(warped_img, valid_area))
# flow_1 = of.Flow.from_transforms([['rotation', 200, 150, -30]], img.shape[:2])
# flow_2 = of.Flow.from_transforms([['scaling', 100, 50, 0.7]], img.shape[:2])
# result = flow_1.combine_with(flow_2, mode=3)
# warped_img, valid_area = result.apply(to_tensor(img, True), return_valid_area=True)
# cv2.imwrite('C:/Users/RVIM_Claudio/Downloads/usage_apply_thames_warped2.png',
#             show_masked_image(warped_img, valid_area))
#
# # Make a circular mask
# shape = (300, 350)
# mask = np.mgrid[-shape[0]//2:shape[0]//2, -shape[1]//2:shape[1]//2]
# radius = shape[0] // 2 - 20
# mask = np.linalg.norm(mask, axis=0)
# mask = mask < radius
#
# # Load image, make two images that simulate a moving telescope
# img = cv2.imread('_static/thames_300x400.jpg')
# img1 = np.copy(img[:, :-50])
# img2 = np.copy(img[:, 50:])
# img1[~mask] = 0
# img2[~mask] = 0
#
# # Make a flow field that could have been obtained from the above images
# flow = of.Flow.from_transforms([['translation', -50, 0]], shape, 't', mask)
# flow.vecs[:, ~mask] = 0
#
# # Apply the flow to the image, setting consider_mask to True and False
# warped_img, valid_area = flow.apply(to_tensor(img1, True), to_tensor(mask), return_valid_area=True)
#
# cv2.imwrite('C:/Users/RVIM_Claudio/Downloads/usage_apply_masked_img1.png', img1)
# cv2.imwrite('C:/Users/RVIM_Claudio/Downloads/usage_apply_masked_img2.png', img2)
# cv2.imwrite('C:/Users/RVIM_Claudio/Downloads/usage_apply_masked_flow.png',
#             flow.visualise('bgr', True, True, return_tensor=False))
# cv2.imwrite('C:/Users/RVIM_Claudio/Downloads/usage_apply_masked_flow_arrows.png',
#             flow.visualise_arrows(60, None, 1, True, True, return_tensor=False))
# cv2.imwrite('C:/Users/RVIM_Claudio/Downloads/usage_apply_masked_img_warped.png',
#             show_masked_image(warped_img, valid_area))
#
# # Make a circular mask with the lower left corner missing
# shape = (300, 400)
# mask = np.mgrid[-shape[0]//2:shape[0]//2, -shape[1]//2:shape[1]//2]
# radius = shape[0] // 2 - 20
# mask = np.linalg.norm(mask, axis=0)
# mask = mask < radius
#
# # Load image, make a flow field, apply masks
# img = cv2.imread('_static/thames_300x400.jpg')
# img[~mask] = 0
# flow_mask = mask.copy()
# mask[150:, :200] = False
# flow_mask[150:, :200] = False
# flow_mask[150:, 260:] = False
# flow = of.Flow.from_transforms([['scaling', 200, 150, 1.3]], shape, 's', flow_mask)
# flow.vecs[:, :, ~mask] = 0
#
# # Apply the flow to the image, setting consider_mask to True and False
# unset_pure_pytorch()
# img_true = flow.apply(to_tensor(img, 'single'), consider_mask=True)
# img_false = flow.apply(to_tensor(img, 'single'), consider_mask=False)
# set_pure_pytorch()
# img_true_pt = flow.apply(to_tensor(img, 'single'), consider_mask=True)
# img_false_pt = flow.apply(to_tensor(img, 'single'), consider_mask=False)
#
# cv2.imwrite('C:/Users/RVIM_Claudio/Downloads/usage_apply_consider_mask_img.png', img)
# cv2.imwrite('C:/Users/RVIM_Claudio/Downloads/usage_apply_consider_mask_flow.png',
#             flow.visualise('bgr', True, True, return_tensor=False)[0])
# cv2.imwrite('C:/Users/RVIM_Claudio/Downloads/usage_apply_consider_mask_flow_arrows.png',
#             flow.visualise_arrows(50, show_mask=True, show_mask_borders=True, return_tensor=False)[0])
# cv2.imwrite('C:/Users/RVIM_Claudio/Downloads/usage_apply_consider_mask_true.png',
#             np.moveaxis(to_numpy(img_true), 0, -1))
# cv2.imwrite('C:/Users/RVIM_Claudio/Downloads/usage_apply_consider_mask_false.png',
#             np.moveaxis(to_numpy(img_false), 0, -1))
# cv2.imwrite('C:/Users/RVIM_Claudio/Downloads/usage_apply_consider_mask_true_pytorch.png',
#             np.moveaxis(to_numpy(img_true_pt), 0, -1))
# cv2.imwrite('C:/Users/RVIM_Claudio/Downloads/usage_apply_consider_mask_false_pytorch.png',
#             np.moveaxis(to_numpy(img_false_pt), 0, -1))
#
# # Load image and pad with a black border
# img = cv2.imread('_static/thames_300x400.jpg')
# pad_img = np.pad(img, ((100, 100), (100, 100), (0, 0)))
#
# # Create a flow field with an undefined area in the lower left corner
# mask = np.ones(img.shape[:2], 'bool')
# mask[100:, :200] = False
# transforms = [['scaling', 100, 50, 1.1]]
# flow = of.Flow.from_transforms(transforms, img.shape[:2], 's', mask)
# flow.vecs[100:, :200] = 0
#
# # Apply the flow field to the padded image considering the flow mask (consider_mask=True), default behaviour
# warped_consider_true = flow.apply(to_tensor(pad_img, True),
#                                   padding=(100, 100, 100, 100), cut=False, consider_mask=True)
#
# # Apply the flow field to the padded image without considering the flow mask (consider_mask=False)
# warped_consider_false = flow.apply(to_tensor(pad_img, True),
#                                    padding=(100, 100, 100, 100), cut=False, consider_mask=False)
#
# show_masked_image(warped_consider_true)
# show_masked_image(warped_consider_false)


# # # # Usage / Padding
# # Load an image
# full_img = cv2.imread('_static/thames.jpg')  # original resolution 600x800
#
# # Define a flow field
# shape = (300, 300)
# transforms = [['rotation', 200, 150, -30], ['scaling', 100, 50, 0.7]]
# flow = of.Flow.from_transforms(transforms, shape)
#
# # Get the necessary padding
# padding = flow.get_padding()
#
# # Select an image patch that is equal in size to the flow resolution plus the padding
# padded_patch = full_img[:shape[0] + sum(padding[:2]), :shape[1] + sum(padding[2:])]
#
# # Apply the flow field to the image patch, passing in the padding
# warped_padded_patch = flow.apply(to_tensor(padded_patch, True), padding=padding)
# cv2.imwrite('C:/Users/RVIM_Claudio/Downloads/usage_padding_padded_warped.png', to_numpy(warped_padded_patch, True))
#
# # As a comparison: cut an unpadded patch out of the image and warp it with the same flow
# patch = full_img[padding[0]:padding[0] + shape[0], padding[2]:padding[2] + shape[1]]
# cv2.imwrite('C:/Users/RVIM_Claudio/Downloads/usage_padding_patch.png', patch)
# warped_patch = flow.apply(to_tensor(patch, True))
# cv2.imwrite('C:/Users/RVIM_Claudio/Downloads/usage_padding_warped.png', to_numpy(warped_patch, True))
#
# # Load an image, define a flow field
# img = cv2.imread('_static/thames_300x400.jpg')
# transforms = [['rotation', 200, 150, -30], ['scaling', 100, 50, 0.9]]
# flow = of.Flow.from_transforms(transforms, img.shape[:2], 's')  # 300x400 pixels
#
# # Find the padding and pad the image
# padding = flow.get_padding()
# padded_img = np.pad(img, (tuple(padding[:2]), tuple(padding[2:]), (0, 0)))
#
# # Apply the flow field to the image patch, with and without the padding
# warped_img = flow.apply(to_tensor(img, True))
# warped_padded_img = flow.apply(to_tensor(padded_img, True), padding=padding, cut=False)
# cv2.imwrite('C:/Users/RVIM_Claudio/Downloads/usage_padding_s_warped.png', to_numpy(warped_img, True))
# cv2.imwrite('C:/Users/RVIM_Claudio/Downloads/usage_padding_s_warped_padded.png', to_numpy(warped_padded_img, True))


# # # # Usage / Source & Target
# # Define a flow field
# shape = (300, 400)
# transforms = [['rotation', 200, 150, -30], ['scaling', 100, 50, 1.2]]
# flow = of.Flow.from_transforms(transforms, shape)
#
# # Get the valid source and target areas
# valid_source = flow.valid_source()
# valid_target = flow.valid_target()
#
# # Load an image and warp it with the flow
# img = cv2.imread('_static/thames_300x400.jpg')
# warped_img = flow.apply(to_tensor(img, True))
#
# cv2.imwrite('C:/Users/RVIM_Claudio/Downloads/usage_source_target_img.png', img)
# cv2.imwrite('C:/Users/RVIM_Claudio/Downloads/usage_source_target_warped_img.png', to_numpy(warped_img, True))
# cv2.imwrite('C:/Users/RVIM_Claudio/Downloads/usage_source_target_source.png',
#             255 * to_numpy(valid_source).astype('uint8'))
# cv2.imwrite('C:/Users/RVIM_Claudio/Downloads/usage_source_target_target.png',
#             255 * to_numpy(valid_target).astype('uint8'))


# # # # Usage / Track
# background = np.zeros((40, 60, 3), 'uint8')
# pts = np.array([[5, 15], [20, 15], [5, 50], [20, 50]])
# flow = of.Flow.from_transforms([['rotation', 0, 0, -15]], background.shape[:2], 's')
# tracked_pts = flow.track(torch.tensor(pts), int_out=True)
# background[pts[:, 0], pts[:, 1]] = 255
# background[tracked_pts[:, 0], tracked_pts[:, 1], 2] = 255
# background = np.repeat(np.repeat(background, 5, axis=0), 5, axis=1)
# bgr = flow.resize(2.5).visualise_arrows(grid_dist=30, show_mask=True, show_mask_borders=True, return_tensor=False)
# bgr = np.repeat(np.repeat(bgr, 2, axis=0), 2, axis=1)
# cv2.imwrite('C:/Users/RVIM_Claudio/Downloads/usage_track_flow.png', bgr)
# cv2.imwrite('C:/Users/RVIM_Claudio/Downloads/usage_track_pts.png', background)
#
# background = np.zeros((40, 60, 3), 'uint8')
# pts = np.array([[5, 15], [20, 15], [5, 50], [20, 50]])
# mask = np.ones((40, 60), 'bool')
# mask[:15, :30] = False
# flow = of.Flow.from_transforms([['rotation', 0, 0, -25]], background.shape[:2], 's', mask)
# tracked_pts, valid_status = flow.track(torch.tensor(pts), int_out=True, get_valid_status=True)
# background[pts[:, 0], pts[:, 1]] = 255
# background[tracked_pts[valid_status][:, 0], tracked_pts[valid_status][:, 1], 2] = 255
# background = np.repeat(np.repeat(background, 5, axis=0), 5, axis=1)
# bgr = flow.resize(2.5).visualise_arrows(grid_dist=30, show_mask=True, show_mask_borders=True, return_tensor=False)
# bgr = np.repeat(np.repeat(bgr, 2, axis=0), 2, axis=1)
# cv2.imwrite('C:/Users/RVIM_Claudio/Downloads/usage_track_flow_with_validity.png', bgr)
# cv2.imwrite('C:/Users/RVIM_Claudio/Downloads/usage_track_pts_with_validity.png', background)


# # # # Usage / Combining
# # Define a flow field
# shape = (300, 400)
# flow_1 = of.Flow.from_transforms([['rotation', 200, 150, -30]], shape)
# flow_2 = of.Flow.from_transforms([['scaling', 100, 50, 1.2]], shape)
# flow_3 = of.Flow.from_transforms([['rotation', 200, 150, -30], ['scaling', 100, 50, 1.2]], shape)
#
# flow_1_result = flow_2.combine(flow_3, mode=1)
# flow_2_result = flow_1.combine(flow_3, mode=2)
# flow_3_result = flow_1.combine(flow_2, mode=3)
# cv2.imwrite('C:/Users/RVIM_Claudio/Downloads/usage_combining_1.png',
#             flow_1.visualise('bgr', True, True, return_tensor=False)[0])
# cv2.imwrite('C:/Users/RVIM_Claudio/Downloads/usage_combining_2.png',
#             flow_2.visualise('bgr', True, True, return_tensor=False)[0])
# cv2.imwrite('C:/Users/RVIM_Claudio/Downloads/usage_combining_3.png',
#             flow_3.visualise('bgr', True, True, return_tensor=False)[0])
# cv2.imwrite('C:/Users/RVIM_Claudio/Downloads/usage_combining_1_result.png',
#             flow_1_result.visualise('bgr', True, True, return_tensor=False)[0])
# cv2.imwrite('C:/Users/RVIM_Claudio/Downloads/usage_combining_2_result.png',
#             flow_2_result.visualise('bgr', True, True, return_tensor=False)[0])
# cv2.imwrite('C:/Users/RVIM_Claudio/Downloads/usage_combining_3_result.png',
#             flow_3_result.visualise('bgr', True, True, return_tensor=False)[0])

# # # # Batching / selecting flows
# # Define three flow objects
# shape = (300, 400)
# flow_1 = of.Flow.from_transforms([['rotation', 200, 150, -30]], shape)
# flow_2 = of.Flow.from_transforms([['scaling', 100, 50, 1.2]], shape)
# flow_3 = of.Flow.from_transforms([['translation', 10, 10]], shape)
#
# # Batch two flows of batch size 1
# flow_batched = of.batch_flows((flow_1, flow_2))
#
# # Batch two flows of batch sizes 2 and 1
# flow_batched = of.batch_flows((flow_batched, flow_3))
#
# # Using the show method without the elem argument automatically selects the first batch element
# flow_batched.show()
#
# # Other batch elements can be indicated as an argument
# flow_batched.show(elem=1)
#
# # Alternatively, a batch element can be selected first and then shown
# flow_batched.select(2).show()


# # # # Flow field for flow doc
# shape = (200, 200)
# flow = of.Flow.from_transforms([['rotation', 300, -50, -30]], shape, 't')
# flow.show_arrows(grid_dist=50)
# flow = of.Flow.from_transforms([['rotation', 300, -50, -30]], shape, 's')
# flow.show_arrows(grid_dist=50)


# # # # Examples for functions not requiring flow class inputs
# # Define Torch tensor flow fields
# shape = (100, 100)
# flow = of.from_transforms([['rotation', 50, 100, -30]], shape, 's')
# flow_2 = of.from_transforms([['scaling', 100, 50, 1.2]], shape, 't')
#
# # Visualise Torch tensor flow field as arrows
# flow_vis = of.show_flow(flow, wait=2000)
#
# # Combine two Torch tensor flow fields
# flow_t = of.switch_flow_ref(flow, 's')
# flow_3 = of.combine_flows(flow_t, flow_2, 3, 't')
#
# # Visualise Torch tensor flow field
# flow_3_vis = of.show_flow_arrows(flow_3, 't')


# # # # Flow field for README
# # Make a flow field and display it
# shape = (300, 400)
# transform = [['rotation', 200, 150, -30]]
# flow = of.Flow.from_transforms(transform, shape)
# # flow.show()
#
# flow_2 = of.Flow.from_transforms([['translation', 40, 0]], shape)
# result = flow.combine_with(flow_2, mode=3)
# result.show(show_mask=True, show_mask_borders=True)
# result.show_arrows(show_mask=True, show_mask_borders=True)
#
# # Alternative option without using the custom flow class
# flow = of.from_transforms(transform, shape, 't')
# of.show_flow(flow)
# flow_2 = of.from_transforms([['translation', 40, 0]], shape, 't')
# result = of.combine_flows(flow, flow_2, mode=3, ref='t')
# of.show_flow(result)  # Note: no way to show the valid flow area (see documentation)
# of.show_flow_arrows(result, 't')  # Note: again no way to show the valid flow area


# # # # Images for the repo "social preview"
# img = cv2.imread('_static/thames_300x400.jpg')[60:-40]
# shape = (200, 400)
# flow = of.Flow.from_transforms([['rotation', 200, 100, -30]], shape)
# warped = flow.apply(to_tensor(img, True))
# cv2.imwrite('C:/Users/RVIM_Claudio/Downloads/img.png', img)
# cv2.imwrite('C:/Users/RVIM_Claudio/Downloads/warped.png', to_numpy(warped, True))
# cv2.imwrite('C:/Users/RVIM_Claudio/Downloads/flow.png', flow.visualise('bgr', return_tensor=False))
# cv2.imwrite('C:/Users/RVIM_Claudio/Downloads/arrows.png',
#             flow.visualise_arrows(50, None, .5, thickness=6, return_tensor=False))


# # # # LOGO
# shape = (400, 300)
# mask = np.mgrid[-shape[0]//2:shape[0]//2, -shape[1]//2:shape[1]//2]
# radius = shape[1] // 2 - 30
# mask = np.linalg.norm(mask, axis=0)
# v_scale = 1.35
# mask = cv2.resize(mask, None, fx=1, fy=v_scale)
# cut = int((400 * (v_scale - 1))//2)
# mask = mask[cut:-cut]
# mask = mask < radius
#
# mask2 = np.mgrid[-shape[0]//2:shape[0]//2, -shape[1]//2:shape[1]//2]
# radius = shape[1] // 2 - 75
# mask2 = np.linalg.norm(mask2, axis=0)
# v_scale = 1.35
# mask2 = cv2.resize(mask2, None, fx=1, fy=v_scale)
# cut = int((400 * (v_scale - 1))//2)
# mask2 = mask2[cut:-cut]
# mask2 = mask2 < radius
#
# mask[mask2] = False
#
# f1 = of.Flow.from_transforms([['translation', -30, -10]], shape, 's')
# f1.vecs[:, :, ~mask] = 0
#
# shape = (400, 300)
# mask = np.zeros(shape, bool)
# mask[40:80, 30:-70] = True
# mask[180:220, 30:-70] = True
# mask[40:-40, 30:80] = True
# f2 = of.Flow.from_transforms([['translation', 30, -10]], shape, 's')
# f2.vecs[:, :, ~mask] = 0
#
# cv2.imwrite('C:/Users/RVIM_Claudio/Downloads/letter_o.png',
#             f1.visualise_arrows(6, scaling=.5, thickness=1, return_tensor=False)[0])
# cv2.imwrite('C:/Users/RVIM_Claudio/Downloads/letter_f.png',
#             f2.visualise_arrows(6, scaling=.5, thickness=1, return_tensor=False)[0])
