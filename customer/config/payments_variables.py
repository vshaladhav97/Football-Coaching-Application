global password_key
global payment_server_url
global VendorEMail

vender_name = "firstkickmanage"

# VendorEMail = "fabio.morais@kuzukogroup.com"
VendorEMail = "info@firstkickfootball.co.uk"

url_type = "live"
password_key = "b64380834a5a8266"

# url_type = "test"
# password_key = "5afd820ca655f9cc"

payment_server_url = 'https://{}.sagepay.com/gateway/service/vspform-register.vsp?VPSProtocol=4.00&TxType=PAYMENT&Vendor={}&Crypt=@'.format(url_type,
                                                                                                                                            vender_name)
