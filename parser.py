from fhirpathpy import evaluate
import json
import glob

ID_FHIR_PATH="CapabilityStatement.id"
LAT_FHIR_PATH="CapabilityStatement.contained.where(resourceType='Organization').address.extension.where(url='http://hl7.org/fhir/StructureDefinition/geolocation').extension.where(url='latitude').valueDecimal"
LONG_FHIR_PATH="CapabilityStatement.contained.where(resourceType='Organization').address.extension.where(url='http://hl7.org/fhir/StructureDefinition/geolocation').extension.where(url='longitude').valueDecimal"
NAME_FHIR_PATH="CapabilityStatement.contained.where(resourceType='Organization').name"
onlyfiles=glob.glob("test/*.json")

#print(onlyfiles)
result={}
final_list=[]
for file in onlyfiles:
    node={"type":"Feature","properties":{"iconSize":[20,20]},"geometry":{"type":"Point"}}
    with open(file) as json_file:
        data = json.load(json_file)
    org_name=evaluate(data,NAME_FHIR_PATH,"")[0]
    
    cs_id=evaluate(data,ID_FHIR_PATH , "")[0]

    lat = evaluate(data, LAT_FHIR_PATH, "")
 #   print(lat)
  
    long = evaluate(data,LONG_FHIR_PATH , "")
  #  print(long)
    #result[cs_id]=[lat[0],long[0],org_name]
    node["properties"]["message"]="<a href='www.google.com'>"+org_name+"</a>"
    node["geometry"]["coordinates"]=[long[0],lat[0]]
    #result[cs_id].append(lat[0],long[0])
    final_list.append(node)
#print(result)
result['type']='FeatureCollection'
result["features"]=final_list

with open("geojson.js", "w") as fout:
        fout.write("const geojson = ")
        json.dump(result, fout)
