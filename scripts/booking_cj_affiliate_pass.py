#!/usr/bin/env python3
"""Route supplied Mametas hotel affiliate links to Booking.com through CJ."""
from pathlib import Path
import base64, json, zlib

ROOT = Path(__file__).resolve().parents[1]
BOOKING_BY_EXPEDIA = json.loads(zlib.decompress(base64.b64decode("eNq1nGuTojwWx7/LVO27lVG8P1VbW9q2l/Yuisq7AAGCIcEERNza776J2jM9s8/uM9CTqq6+QGv9CMnJ//zPwX99CZIk5n98/QqvMXQR0BwafQWehzACCeRfAUmQDXkloAnEzx8VG2IsjjF0gVybmfVeYqEvf3x7qyzLtNP5lnvh/d0cjJxTpVatddrNRrtVqTXb9Yb49Z8pw/+4v+Zv9d7f9KH4kq+0KT0h4suXiiNGABisjOMOy5POl78XxGU0B7jyPKjN155+vAyVki5co1azPwlqZWE7XvpKQVP4FufmX4M6gJDvnMB5nwJ5JQKMIZokFRDZgHPgwpS9X0IlTAGpyEkSI8K1KuxtB7Ol0gtqhWne6RS9IMGaVDLxDTLyvLSQpozA73djs51ca6uxUnj7duobaViUXvxF41zejADhhJLK47Q2mBMc8oZS5NdF923hFyeOK+63WWJD4ASPU1rbs6zh2VLKDF7scftWnJl9HNwpcIDbWisFHR4BInpx0AskLuKBBiYLa/qaKGVs9rvuNS/K6IlNo8IheN9LnoOabjz9jNUusnlzDfRaUeBnvJPBDoo3wbDiM5BXXIBtRInG2oNzjt+UgpvUNBfG58EjEIpIh5z3Qb+F1yXuxkrZJ/1THGSDcvCuxE4owlDjHGLaVCsz7FHQX9KwNGvMqFiADtRWt5jPzlztBp7v2pOwWQ4WRTFkSEgOHzCaxlBrzszgGraVEnO2mRwHk3LEIRUzQOsNto3lLVOK6bWocbqUpBSyB2jZboYXcKF2h5iHYz0pR4lB5YKw+H7fjd91jh+1m25VrerMxrpuBJ+kjilLPogIHgMNBlX7UJsqZXejmrGCv5+dTM+rvA3VJlA6OQ7NdUl4KDcMGzIG3k9QR7wpFNL/ljJtOq25p4Zatam/Ue98VMPvoHR79NVmJ+5qVt1fS/Pz1NVOut+xxrraYZ6g5k0vi8krGHHIKOFyN4xo6svkz+3MPdJQG7NjU889c1sOPBKpa0QFORY642jjKGpHSmlH+8kkC8vCsgQReNPGqNcfNNSGa2eIiPFWDvQCGRZJDNSuWb16Ns9KQbd0e2R+SdB7YOY0DsT/T3HitJdqY1nSMYa3TVHYMPvuuDz1e667vJPW1abMdeslOqOitGJEcUrgxzjgD+c9BiZqMyXfPmWkBGyMgdDtY3hhk2tXKeI+uxxNr3De/Mg7iftj2nxIJ3lrX1UKvHaub9V5Cd4I3B0qF8m46ucvb9XZq1LSsLs1vbhwrklPJ/rBUZNnHEgSBjWK26ule1G7wDrRpsaKMjPIkStzzYcZL+evD7UGN4yoaivljQBNt6+Fee8G9zMUVHyKPXkJQgxrtnVt9ZHaieHlJ6PR/WtmH3COyDvzKbXhc7lxsZMllYTRWOy8nRjP2mu1yQY2SO34CztvRAlw6P9xsyPxqkRKXwLFvRPTmhKts2S9BqJKL+CwuZgiISt4AU4gDoL0bvyI9DQQ8VjsIRXKNI6XzoqotYcbZG7OzoWZKU4jO+VidpME3t1iqvFjy8gsoHYnSb0ZIL8FNycn4wX1leLu+MlZrP2ivB5ATKL+wDsOdRLV1aZsw2gGB25R3O/GJSUuk+WjTdfNiVqRpqe4222VRo0BQz/Oh6E5dlevJ7Ub37HmoHo56ACyCCViy/uBug5ov3VUmxLVamG/UZKagJhiKALwxF5uah21wzvpmPps/knQa8sndUOtANqcL3uQliWll8c292EadPT9TH9tKYVe7TvHXzEy/4z57gHG4J5xdNz19tjpqZXFL/xwSEefhz0PzaHDmdoaDHZHzW45VoYuoAIEr7RVL03YXC3VihxrSqYtWA72AoRCdmQRHMMUvitkKd4iIZGFZNOcYbzMcKj0Cmg0WdT6Ja8AOQll4n+BOeoZh65ihy9sm7QoKLKRHNlzCm0m7QhZ8Hg4aFrfCHbBeqYWunnWu7dS0DzJpaH6UOzv+eiuj9IRUVslX0+t09hfF4X+EIArNsjfV+Qzx/OWo/Gb2npoQs6rHBXFjhmSi5DLYgBDTiDOulp7ZbZuwFGK297saoNFUdwkkAl4bt9blGS8Q5ABbW3s6qep2mSDDVe911tSFPhhrvqQQI641qCbKbPURjTz4vljHX0OFOxHLc9UKyGM827Q7Vm/AvpwTX6W7e/G6mD62l3P1E7XpmNb9i84awQ58FuzIAEkAexurt5A5fspDQ+PITgESomP0anqNosR25SL9Jh+QL1Liea41/AV6x6er7PlphjuR0PYTe+bmyetnkRrRt6866vtSuL2Ge+CYsQP1lbjPsJafQPHM75SSnl1dzguR9nSWmHUXrfUluZbg2TVhWUAgQgA7DGS/txdD/Zq45VXXQZ5WAqUSw0ji2yOSCS01pZWjSlW24ddZSjYlIK9pQwCLaXr28ZXW63ipDXHtTKQtjRJZbrjQ21+zAwwVttttCFmc7T/LClIPT1x1a53cmqSQbYshZoDWQm6L6h187KbzdQWrWNjuTCP1TKoz5ZkzdqYe56q7QkxD3zYXXyG0uZJbQXVCpTYJedatxQljZJ7ofp+41f1hr901Nq1KTaGPPw867a768xXat253nC4qNeaZWDh1RF/IMruDyiAOM6dFCciumr1Se7PXnZqjVpj2d56Zbg9TNm9tHof5LHfGuytgdo+m3T60p24ZWBl7wJkNOVP3M54e/UHhlrc+m6Bq7+DFoFlADBR23pnn9rDN1oKVzZdoAhgF/3XHN6f8/3krNaLmY3cTbIZlkQPQCQ2X81rI2ec7dWmh+fhwApKchLoMygSLw1OrZflUW0rQHwYwsFLOVKRIAopi1zZuCtN8RRrW2MyjzO1jsalNeTnebMscwQ5T/0Ucu3U6Vd1xY0L9eNg60dlWCPAxH6BEdGMRO8vXbV2obdt2H78Oc4U1/zuRG16WPXDUzgtw3k/4lCpF+5tznz9OjmM1Nb4r62ofjyVoX2UP94dzZUzNoCv1tHM+ivdmS0+D3vN9HVD76h1s2DQIccyrLKiVIHEfcyHmNEIEuBC7XJrneKh2scYG4utNTsUpM5BklQY9IUEy5/QAAPEn01BHxuaNKsV5n6ktg/EiuzX2CyoJD/WcGQKjBFMKzxlAp9prcMqjV21Rd/d2I6u12LQ0gCXliJ83+c088Wsz2dq1+HUyEdoXZBUBDUayfZyaXzKRlPZxiJWoxBmPatfnXXU5sSW7dT1cWHmRxuhFA5PI7yWNur0oLar7W2f14NLYdYLZAJXftCDtklDls3V5u+jU30UeEUpucT0Bam8/99HV+v3U903TbUFR7BpNAqqMjFlOSUVgG3AvtfPZ+N4dkvUeg6X9pgZb9OiuBGo8ABiEXCfvti5Ay2zqRQV1tFlW1BE3B8SrtgYECeAWiPeTK2lWqE7D1i8eiXFMB9Vxm83Hge675hztTLHaBz2BRdWBrE4+16te3OsXhir7aSB/LKoNz9DCXjdsPhIbXLT68WnX0humFg3SXpvzP/Z/hD6CzD5WFS1adz06Kb23h+B1e1fywM/5qskhjLlfTbA+27QaMap2gmxbh52oAy5APYgi2TaI9JeLnt9PC9/W/UaivtmxpNg+AvtzR+fJfjzvneZsQPmyo9t0Gh1ldYytXtD3Ec9b1WO/Kcm4h8elKhPDyeDx4pbn1dmkMHfD99/dTLTU+v7eiPd7oWfYb8/Un7f8xKSZrWJ2hJwF/ccbH2G93HmUbkW7AlgiUjktMXaPTgrtR2EznERRJ+aKBzebj9OkgxHl6PlqtXvxsivtce9cuRikJ/J3HeJ/ITfDZy3bKG2fFR/ue5IUhKdpvLjw2CiufXGjc3UKpDxctVtlQzfsRzh5yzRmo6+Myy1c3mzGpuZ84uwsmXwiqI/sYZjgCOxy8gnibvn2UJtHaZbP16706LM/3s12rmN6U9B+9ZLI25t1dbDh62XeefLv/8Drjh7sw==")).decode())
TEXT_SUFFIXES = {".html", ".json", ".xml", ".js"}
SKIP_TOP_LEVEL = {".git", ".github", "docs", "scripts", "data", "lesnicoises-v8-no-mercy-update", "lesnicoises-v8-no-mercy-update 2"}
COPY_REPLACEMENTS = (
    ("Ce lien mène directement vers l’hôtel sur Expedia.", "Ce lien mène directement vers l’hôtel sur Booking.com."),
    ("Ce lien mène directement vers l'hotel sur Expedia.", "Ce lien mène directement vers l'hotel sur Booking.com."),
    ("Ce lien mène directement vers l'hôtel sur Expedia.", "Ce lien mène directement vers l'hôtel sur Booking.com."),
    ("This link goes directly to the hotel on Expedia.", "This link goes directly to the hotel on Booking.com."),
    ("Voir les tarifs sur Expedia", "Voir les tarifs sur Booking.com"),
    ("Voir les prix sur Expedia", "Voir les prix sur Booking.com"),
    ("See rates on Expedia", "See rates on Booking.com"),
    ("Check rates on Expedia", "Check rates on Booking.com"),
    ("View rates on Expedia", "View rates on Booking.com"),
    ("lien Expedia affilié", "lien Booking.com affilié"),
    ("liens Expedia.", "liens Booking.com."),
    ("Expedia affiliate link", "Booking.com affiliate link"),
    ("Expedia affiliate links", "Booking.com affiliate links"),
)

def public_text_files():
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        rel = path.relative_to(ROOT)
        if rel.parts and rel.parts[0] in SKIP_TOP_LEVEL:
            continue
        yield path
    hotel_data = ROOT / "data" / "hotels"
    if hotel_data.is_dir():
        yield from (p for p in hotel_data.glob("*.json") if p.is_file())

def process(path):
    text = path.read_text(encoding="utf-8")
    original = text
    replacements = 0
    for expedia_url, booking_url in BOOKING_BY_EXPEDIA.items():
        for variant in (expedia_url, expedia_url.removeprefix("https://")):
            count = text.count(variant)
            if count:
                text = text.replace(variant, booking_url)
                replacements += count
    if not replacements:
        return 0
    for before, after in COPY_REPLACEMENTS:
        text = text.replace(before, after)
    if text != original:
        path.write_text(text, encoding="utf-8")
    return replacements

def main():
    changed, total, seen = [], 0, set()
    for path in public_text_files():
        if path in seen:
            continue
        seen.add(path)
        count = process(path)
        if count:
            changed.append(path.relative_to(ROOT).as_posix())
            total += count
    print(f"Booking/CJ affiliate pass updated {len(changed)} files and replaced {total} Expedia affiliate URL occurrence(s).")
    for rel in changed:
        print(rel)

if __name__ == "__main__":
    main()
