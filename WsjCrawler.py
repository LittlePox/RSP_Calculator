from Crawler import Crawler
from ProductQuote import ProductQuote
from datetime import timedelta
from Product import Product
from urllib import request
from datetime import datetime
import time
import gzip


class WsjCrawler(Crawler):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': 'wsjregion=na%2Cus; gdprApplies=false; ccpaApplies=false; ab_uuid=df510102-7f90-43a0-b57a-30d1126c8f6d; usr_bkt=ixi4E5ylqa; _pubcid=75a36fd9-80fe-4703-af16-7b62c9b008e4; _pubcid_cst=DCwOLBEsaQ%3D%3D; _sp_su=false; _lr_geo_location_state=KKC; _lr_geo_location=HK; AMCVS_CB68E4BA55144CAA0A4C98A5%40AdobeOrg=1; _ncg_domain_id_=eff62b61-dacc-4bb4-9490-4baa781c92f1.1.1722403704.1753939704; _dj_ses.9183=*; _ga=GA1.1.1950499000.1722403705; ajs_anonymous_id=d3ce4dc5-8c34-4bc5-a885-fb6527799d68; _fbp=fb.1.1722403705184.485592556; _meta_facebookTag_sync=1722403705184; s_cc=true; AMCV_CB68E4BA55144CAA0A4C98A5%40AdobeOrg=1585540135%7CMCIDTS%7C19936%7CMCMID%7C23505481477963330581263765503866092172%7CMCAAMLH-1723008504%7C3%7CMCAAMB-1723008504%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1722410905s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C4.4.0; _gcl_au=1.1.1374935136.1722403705; _ncg_sp_ses.5378=*; _ncg_id_=eff62b61-dacc-4bb4-9490-4baa781c92f1; _meta_cross_domain_id=6daae64c-1a67-4a1b-bf3c-552a648f06e5; _meta_cross_domain_recheck=1722403705495; _ncg_g_id_=71205c6d-6049-45f3-a79e-78c8490d18d8.3.1722403705.1753939704; _scor_uid=5ed5f9be43ab4511800e5a4a3a1ec7fd; _scid=1e5c764a-1793-49f3-8ccf-05f3c9bc7d3d; _scid_r=1e5c764a-1793-49f3-8ccf-05f3c9bc7d3d; _dj_sp_id=47d38379-3be2-4a78-ae6e-04723ce2c2b2; _fbp=fb.1.1722403705184.485592556; _pcid=%7B%22browserId%22%3A%22lz9ep1dwpb5hgzln%22%7D; cX_P=lz9ep1dwpb5hgzln; _pin_unauth=dWlkPVpEbGpPVGMyTUdRdFlqRTFOQzAwTTJFMUxXSXhNVFV0WmpnMU5tUm1Zemt4T1RGaQ; _ScCbts=%5B%5D; cX_G=cx%3A1r70popgvwjhek1l6us3z2nez%3Aoqid7fuyfu9l; _sctr=1%7C1722355200000; permutive-id=8537d0af-1324-454c-876c-8202a4da3eec; djcs_route=675b303c-a487-4137-aab1-67cb85144da5; __gads=ID=70241565235906f2:T=1722403708:RT=1722405459:S=ALNI_MZ72Gp8-G1HhxDjTSoZAQ60WeWhpw; __gpi=UID=00000ec368e4d03c:T=1722403708:RT=1722405459:S=ALNI_MYEyiaOp373rwCEfe2Von2DEWuxPw; __eoi=ID=0a05be3d9cc166a8:T=1722403708:RT=1722405459:S=AA-AfjYay8sJMWntri4MUBtP1i5z; usr_prof_v2=eyJpYyI6NH0%3D; DJSESSION=country%3Dhk%7C%7Ccontinent%3Das%7C%7Cregion%3Dkkc; vcdpaApplies=false; regulationApplies=gdpr%3Afalse%2Ccpra%3Afalse%2Cvcdpa%3Afalse; djvideovol=1; _pctx=%7Bu%7DN4IgrgzgpgThIC4B2YA2qA05owMoBcBDfSREQpAeyRCwgEt8oBJAEzIE4AmHgZgEYAHADZ%2BvQQFYuAFhEcADPJABfIA; utag_main=v_id:01910742cdbf0020ee9a46523d5c0506f004006700fb8$_sn:1$_se:2$_ss:0$_st:1722407264926$ses_id:1722403704256%3Bexp-session$_pn:2%3Bexp-session$_prevpage:WSJ_Home_US%20Home%20Page%3Bexp-1722409064937$vapi_domain:wsj.com; _dj_id.9183=.1722403705.1.1722405465..1e103767-bbb7-4bf4-ae6e-7f803b74cf65..c89e488b-86cb-4b0e-817b-f17d8e4216d9.1722403705008.2; _ncg_sp_id.5378=eff62b61-dacc-4bb4-9490-4baa781c92f1.1722403705.1.1722405465.1722403705.af23d1de-e726-43d1-b20e-2447c00c44e6; s_tp=9375; s_ppv=WSJ_Home_US%2520Home%2520Page%2C26%2C26%2C2433; _uetsid=b5f4ab104efd11efa5fae5087d084814; _uetvid=b5f4c5104efd11ef9d26d5b68cb7407f; _rdt_uuid=1722403704952.c81b0616-c403-4402-a579-049cbbcdd034; datadome=5bc5AHI9nXOKQTKyDH89ToOckz_7cFt7J7YnhaWoiz5xnRCAeGN5HhaKmCOvlPFPXMfr~20ynIFqfH04PvwYXMha7VRZzPa2_goJx56Hdm7J2I7DAp_6Ot4djWdN~r_P',
        'Priority': 'u=0, i',
        'Sec-Ch-Ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
    }

    def crawl_by_dates(self, product, start, end):
        str_start = start.strftime('%m/%d/%Y')
        str_end = end.strftime('%m/%d/%Y')
        url = r'https://www.wsj.com/market-data/quotes/{0}/historical-prices/download?MOD_VIEW=page&num_rows=10000&range_days=10000&startDate={1}&endDate={2}'.format(
            product.wsjTicker, str_start, str_end
        )
        print('Crawling {0}...'.format(url))

        #proxy = request.ProxyHandler({'https': '127.0.0.1:7890'})
        #opener = request.build_opener(proxy)
        #request.install_opener(opener)

        for i in range(0, 5):
            print('trial {0}'.format(i))
            try:
                req = request.Request(url, headers=WsjCrawler.headers)
                content = request.urlopen(req)
                if content.info().get('Content-Encoding') == 'gzip':
                    # Decompress the gzip content
                    with gzip.GzipFile(fileobj=content) as gzip_response:
                        url_content = gzip_response.read().decode('UTF-8')
                else:
                    url_content = content.read().decode('UTF-8')
                lines = url_content.splitlines()[1:]
                res = []
                for line in lines:
                    res.append(self.convert_to_quote(product, line))
                return res
            except Exception as e:
                print(e)
                time.sleep(3 * (i + 1))
        return []

    def convert_to_quote(self, product, line):
        cells = line.split(', ')
        cob_date = datetime.strptime(cells[0], '%m/%d/%y').date()
        close = float(cells[4])
        nav = close
        return ProductQuote(product.id, cob_date, close, nav)
