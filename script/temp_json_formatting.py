import json
import datetime



# Creates a list of all the region groups
def list_region_groups():
  res = []

  for key in image_output.keys():
    region_group = {
        "id": key,
        "regions": list_regions(image_output[key], key)
    }
    res.append(region_group)

  return res

# Creates a list of all the regions of a region group
def list_regions(regions, media_id):
  res = []

  for region in regions[0]:
    val = {
        "media_id": media_id,
        "box": normalize_coordinates(region.cpu().numpy().tolist(), regions[1][0], regions[1][1])
    }
    res.append(val)
  
  return res

# Takes x or y coordinates and normalizes these to a [0-1] scale.
# coordinates: list of coordinates which will be transformed
# max: the maximum value a coordinate can have
# min: the minimum value a coordinate can have
def normalize_coordinates(coordinates, max_x, max_y):
  x_cords = normalize_coordinates_helper([coordinates[0],coordinates[2]], max_x)
  y_cords = normalize_coordinates_helper([coordinates[1],coordinates[3]], max_y)

  res = [x_cords[0], y_cords[0], x_cords[1], y_cords[1]]

  if max(res) > 1:
    print("mistake with:", coordinates, max_x, max_y)

def normalize_coordinates_helper(coordinates, max):
  res = []
  min = 0
  dif = max - min

  for cord in coordinates:
    val = (cord - min) / dif
    res.append(val)

  return res

# Returns a list of predictions per region group
def list_predictions():
  res = []

  for key in image_output.keys():
    value = {
        "region_group_id": key,
        "taxa": list_taxon(image_output[key][2])
    }
    res.append(value)

  return res

# Returns a list of taxons per prediction
def list_taxon(scores):
  res = []

  for score in scores:
    value = {
        "probability": score,
        "scientific_name_id": -1,
        "scientific_name": "Homo Sapien" 
    }
    res.append(value)

  return res

res = {
    "generated_by": {
        "datetime": datetime.datetime.now().isoformat(),
        "version": -1,
        "tag": -1
    },
    "media": list(image_output.keys()),
    "region_groups": list_region_groups(),
    "predictions": list_predictions(),
}

print(json.dumps(res))