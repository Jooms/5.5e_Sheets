#!/usr/bin/env python3
import zlib, struct, sys

def load(path):
    data=open(path,'rb').read()
    assert data[:8]==b'\x89PNG\r\n\x1a\n'
    i=8; W=H=bd=ct=None; idat=b''
    while i<len(data):
        ln=struct.unpack('>I',data[i:i+4])[0]; typ=data[i+4:i+8]
        chunk=data[i+8:i+8+ln]
        if typ==b'IHDR':
            W,H,bd,ct=struct.unpack('>IIBB',chunk[:10])
        elif typ==b'IDAT':
            idat+=chunk
        elif typ==b'IEND':
            break
        i+=12+ln
    raw=zlib.decompress(idat)
    ch={0:1,2:3,3:1,4:2,6:4}[ct]
    bpp=ch
    stride=W*bpp
    out=bytearray(); prev=bytearray(stride)
    pos=0
    for y in range(H):
        f=raw[pos]; pos+=1
        line=bytearray(raw[pos:pos+stride]); pos+=stride
        if f==1:
            for x in range(bpp,stride): line[x]=(line[x]+line[x-bpp])&255
        elif f==2:
            for x in range(stride): line[x]=(line[x]+prev[x])&255
        elif f==3:
            for x in range(stride):
                a=line[x-bpp] if x>=bpp else 0
                line[x]=(line[x]+((a+prev[x])>>1))&255
        elif f==4:
            for x in range(stride):
                a=line[x-bpp] if x>=bpp else 0
                b=prev[x]; c=prev[x-bpp] if x>=bpp else 0
                p=a+b-c; pa=abs(p-a); pb=abs(p-b); pc=abs(p-c)
                pr=a if (pa<=pb and pa<=pc) else (b if pb<=pc else c)
                line[x]=(line[x]+pr)&255
        out+=line; prev=line
    return W,H,bpp,bytes(out)

(w1,h1,b1,p1)=load(sys.argv[1])
(w2,h2,b2,p2)=load(sys.argv[2])
print("dims",w1,h1,b1,"vs",w2,h2,b2)
n=min(len(p1),len(p2))
diff=0; maxd=0; nz=0
for i in range(0,n, b1):  # sample first channel of every pixel
    d=abs(p1[i]-p2[i]); diff+=d
    if d>maxd: maxd=d
    if d>8: nz+=1
px=n//b1
print(f"mean abs diff (R chan): {diff/px:.3f}   max: {maxd}   pixels diff>8: {nz} ({100*nz/px:.2f}%)")
