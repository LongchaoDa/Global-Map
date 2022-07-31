import requests
import pandas as pd
import json

"""
 get data from dp address
 @param dpAddress  DP Address访问地址
"""
import requests
import pandas as pd
import json

"""
 get data from dp address
 @param dpAddress  DP Address访问地址
"""
def get_data(dpAddress):
    url = "https://citybrain.org/api/getData"
    data = {"dpAddress": dpAddress, "payload": ""}
    response = requests.post(url=url, headers={"content-type": "application/json"}, json=data)
    if response.status_code == requests.codes.ok:
        resp = response.json()
        if resp["code"] == 200:
            sourceResp = json.loads(resp["data"])
            print(pd.json_normalize(sourceResp["data"]))
        else:
            print(resp["code"])
            print(resp["message"])
    else:
        print(response.status_code)

"""
 get meta_data from dp address
"""
def get_meta_data(dpAddress):
    url = "https://citybrain.org/api/kernel/dp-address"
    p = {"dpAddress": dpAddress}
    response = requests.get(url, params=p)
    if response.status_code == requests.codes.ok:
        resp = response.json()
        if resp["code"] == 200:
            print(resp["data"]["route"]["path"])
            print(resp["data"]["transfer"]["endpoint"][0])
            path = "https://" + resp["data"]["transfer"]["endpoint"][0] + resp["data"]["route"]["path"]
            newurl = path[0:path.index("page_size")] + "page_size=1"
            resp1 = response = requests.get(newurl)
            print(resp1.json()["data"])
        else:
            print(resp["code"])
            print(resp["message"])
    else:
        print(response.status_code)




if __name__ == "__main__":
    data_raw = get_data("158B8F97EA421000")
    # data_meta = get_meta_data("158B8F97EA421000")


