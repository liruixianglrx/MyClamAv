import requests

class VirusTotalScanner:
    def __init__(self):
        self.api_key = "39e8c7fde78d0010b93247155fdc541e0d87198fcf06d8ffeedf80bf8073ab0d"
        self.base_url = "https://www.virustotal.com/vtapi/v2/"

    def scan_file(self,file_path):
        self.upload_file(file_path)
        return self.get_file_report()

    def upload_file(self, file_path):
        with open(file_path, "rb") as file:
            files = {"file": (file_path, file)}
            params = {"apikey": self.api_key}

            response = requests.post(self.base_url + "file/scan", files=files, params=params)
            result = response.json()
            self.sha1=str(response.json()['sha1'])
            return result

    def get_file_report(self):
        params = {"apikey": self.api_key, "resource": self.sha1}
        response = requests.get(self.base_url + "file/report", params=params)
        result = response.json()
        response_code = result['response_code']
        while (response_code == -2):
            sleep(2)
            response = requests.get(self.base_url + "file/report", params=params)
            result = response.json()
            response_code = result['response_code']

        nums = result['positives']
        total = result['total']
        return nums,total

    def scan_url(self,url):
        self.upload_url(url)
        return self.get_url_report(url)
    def upload_url(self, url):
        params = {"apikey": self.api_key, "url": url}
        response = requests.post(self.base_url + "url/scan", params=params)
        result = response.json()
        return result

    def get_url_report(self, url):
        params = {"apikey": self.api_key, "resource": url}
        response = requests.get(self.base_url + "url/report", params=params)
        result = response.json()
        response_code = result['response_code']
        while (response_code == -2):
            sleep(2)
            response = requests.get(self.base_url + "file/report", params=params)
            result = response.json()
            response_code = result['response_code']
        nums = result['positives']
        total = result['total']
        return nums,total

    def scan_ip_or_domain(self, ip_or_domain):
        params = {"apikey": self.api_key, "ip": ip_or_domain}
        response = requests.get(self.base_url + "ip-address/report", params=params)
        result = response.json()
        return result

