# ean_label.py — standard etykiet EAN (PCBLAB). Użycie: python3 ean_label.py OUT.pdf W H "SKU;EAN" ["SKU;EAN" ...] [--imp]
import io, sys
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
L='0001101 0011001 0010011 0111101 0100011 0110001 0101111 0111011 0110111 0001011'.split()
G='0100111 0110011 0011011 0100001 0011101 0111001 0000101 0010001 0001001 0010111'.split()
R='1110010 1100110 1101100 1000010 1011100 1001110 1010000 1000100 1001000 1110100'.split()
P='LLLLLL LLGLGG LLGGLG LLGGGL LGLLGG LGGLLG LGGGLL LGLGLG LGLGGL LGGLGL'.split()
DJ='/usr/share/fonts/truetype/dejavu/'
IMP=["Importer: PCBLAB Aneta Kopeć-Dziura","Wola Rzędzińska 252B/3  |  https://pcblab.io"]
def ok(e): return len(e)==13 and e.isdigit() and (10-sum(int(e[i])*(3 if i%2 else 1) for i in range(12))%10)%10==int(e[12])
def bc(e, dm=45):  # obraz kodu: skala 3, strefa ciszy 11, przedłużenie strażników 10 modułów, cyfry 24 px bold
    b='101'+''.join((G if P[int(e[0])][i]=='G' else L)[int(d)] for i,d in enumerate(e[1:7]))+'01010'+''.join(R[int(d)] for d in e[7:])+'101'
    S,q=3,11; gp=set(range(3))|set(range(45,50))|set(range(92,95)); dh=dm*S; ba=dh+30
    f=ImageFont.truetype(DJ+'DejaVuSans-Bold.ttf',24); d0=ImageDraw.Draw(Image.new('RGB',(9,9))); bb=d0.textbbox((0,0),'0',font=f); h=bb[3]-bb[1]
    im=Image.new('RGB',((len(b)+2*q)*S,max(ba,dh+h+10)),'white'); dr=ImageDraw.Draw(im)
    for i,c in enumerate(b):
        if c=='1': dr.rectangle([(q+i)*S,0,(q+i)*S+S-1,(ba if i in gp else dh)-1],fill='black')
    y=dh+5; qs=q*S
    def t(s,cx):
        w=dr.textbbox((0,0),s,font=f); dr.text((cx-(w[2]-w[0])//2,y),s,fill='black',font=f)
    w0=dr.textbbox((0,0),e[0],font=f); dr.text((max(0,qs//2-(w0[2]-w0[0])//2),y),e[0],fill='black',font=f)
    t(e[1:7],qs+9+63); t(e[7:],qs+9+126+15+63); return im
def label(c, sku, e, W=70, H=50, foot=None):
    assert ok(e), 'Błędny EAN '+e
    pw,ph=W*mm,H*mm; d=(W,H)==(70,50); M=2.5*mm if d else 2*mm; VM=2.5*mm if d else 1.5*mm
    BW=62*mm if d else pw-2*M; GAP=3*mm if d else 1.2*mm; foot=foot or []
    FS,FL=4.5,5.2; fh=(len(foot)-1)*FL+FS*.75+1*mm if foot else 0
    fs=min(22.0 if d else min(22.0,H*.6), 13.0 if foot else 99)
    while c.stringWidth(sku,'Helvetica-Bold',fs)>pw-2*M: fs-=.5
    assert fs>=6, 'SKU nie mieści się w jednej linii'
    sh=fs*.72 if foot else fs; avail=ph-2*VM-sh-GAP-fh; dm=45; im=bc(e,dm)
    while BW*im.size[1]/im.size[0]>avail and dm>8: dm-=1; im=bc(e,dm)   # skracamy tylko kreski, nigdy długość
    bh=BW*im.size[1]/im.size[0]
    if foot:
        y0=(ph-(fh+bh+GAP+sh))/2
        for i,l in enumerate(reversed(foot)):
            assert c.stringWidth(l,'DejaVu',FS)<=pw-2*M; c.setFont('DejaVu',FS); c.drawString((pw-c.stringWidth(l,'DejaVu',FS))/2,y0+i*FL,l)
        by=y0+fh
    else: by=(ph-(fs+GAP+bh))/2
    buf=io.BytesIO(); im.save(buf,'PNG'); buf.seek(0)
    c.drawImage(ImageReader(buf),(pw-BW)/2,by,width=BW,height=bh)
    c.setFont('Helvetica-Bold',fs); c.drawString((pw-c.stringWidth(sku,'Helvetica-Bold',fs))/2,by+bh+GAP,sku)
if __name__=='__main__':
    pdfmetrics.registerFont(TTFont('DejaVu',DJ+'DejaVuSans.ttf'))
    a=[x for x in sys.argv[1:] if x!='--imp']; out,W,H=a[0],float(a[1]),float(a[2])
    c=canvas.Canvas(out,pagesize=(W*mm,H*mm))
    for it in a[3:]:
        s,e=it.split(';'); label(c,s,e,W,H,IMP if '--imp' in sys.argv else None); c.showPage()
    c.save(); print('OK',out)
