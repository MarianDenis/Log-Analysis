def append_logs(logs):
    intrusion_dict = {}
    intrusion_dict['client_ip'] = '109.98.191.212'
    intrusion_dict['method'] = 'GET'
    intrusion_dict['request'] = '/rezultate_admitere.php'
    intrusion_dict['response_code_class'] = '200'
    intrusion_dict['response_code'] = '200'
    intrusion_dict['query'] = "facultate=AC'+OR+1=1"
    intrusion_dict['data_transfered'] = '942'
    for _ in range(3):
        logs.append(intrusion_dict)
    intrusion_dict = {}
    intrusion_dict['client_ip'] = '109.88.171.211'
    intrusion_dict['method'] = 'GET'
    intrusion_dict['request'] = '/rezultate_admitere.php'
    intrusion_dict['response_code_class'] = '200'
    intrusion_dict['response_code'] = '200'
    intrusion_dict['query'] = "facultate=AC'+union+select+1,2,3"
    intrusion_dict['data_transfered'] = '13942'
    for _ in range(2):
        logs.append(intrusion_dict)
    intrusion_dict = {}
    intrusion_dict['client_ip'] = '88.98.141.198'
    intrusion_dict['method'] = 'GET'
    intrusion_dict['request'] = '/insecure-website.php'
    intrusion_dict['response_code_class'] = '200'
    intrusion_dict['response_code'] = '200'
    intrusion_dict['query'] = "products?category=Gifts'--"
    intrusion_dict['data_transfered'] = '242'
    for _ in range(1):
        logs.append(intrusion_dict)
