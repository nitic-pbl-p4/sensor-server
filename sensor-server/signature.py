import rsa
 
pub_file_path = "pub_key.pem"
private_file_path = "private_key.pem"
 
(pub_key, private_key) = rsa.newkeys(2048)
 
with open(pub_file_path, 'wb+') as f:
    pub_str = pub_key.save_pkcs1('PEM')
    f.write(pub_str)
 
with open(private_file_path, 'wb+') as f:
    private_str = private_key.save_pkcs1('PEM')
    f.write(private_str)