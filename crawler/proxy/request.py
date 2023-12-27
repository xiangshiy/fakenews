import mitmproxy

def request(flow):
    flow.request.headers["User-Agent"] = "MitmProxy"
    from urllib.parse import urlparse, parse_qs

    url = 'https://www.douyin.com/video/1234567890123456?_d=1&_signature=abcdefg&_timestamp=1234567890'
    parsed_url = urlparse(url)
    vid = parse_qs(parsed_url.query).get('_vid')
    if vid:
        print(vid[0])