import cairosvg

W, H = 1100, 640
s = []
s.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Noto Sans CJK KR, Malgun Gothic, sans-serif">')
s.append(f'<rect width="{W}" height="{H}" fill="#f7f7f5"/>')
s.append('<text x="24" y="36" font-size="22" font-weight="bold" fill="#222">MPU-6050 (GY-521) ↔ Nucleo-F446RE 배선</text>')
s.append('<text x="24" y="60" font-size="13" fill="#555">브레드보드 f1~f8에 모듈 핀 꽂고 납땜 → g열에서 점퍼선(수) 뽑아 Nucleo 암헤더로. 전원은 3.3V (5V 아님).</text>')

# ---------- breadboard ----------
bx, by = 40, 110
cols = 14          # show 14 columns
pitch = 22
bw = 60 + cols*pitch
bh = 300
s.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="8" fill="#e9e6dc" stroke="#b9b5a8"/>')
s.append(f'<text x="{bx+8}" y="{by-8}" font-size="13" fill="#555">브레드보드 (위쪽 블록 일부)</text>')
# power rails top
for i,(y,lab,col) in enumerate([(by+16,'+','#d33'),(by+30,'−','#36c')]):
    s.append(f'<line x1="{bx+40}" y1="{y}" x2="{bx+bw-20}" y2="{y}" stroke="{col}" stroke-width="1.5"/>')
    s.append(f'<text x="{bx+22}" y="{y+4}" font-size="12" fill="{col}">{lab}</text>')
    for c in range(cols):
        s.append(f'<circle cx="{bx+50+c*pitch}" cy="{y}" r="2.6" fill="#777"/>')
s.append(f'<text x="{bx+bw-140}" y="{by+46}" font-size="10" fill="#888">전원 레일 (지금은 안 씀)</text>')

rows = ['j','i','h','g','f']
ry0 = by+70
# column numbers
for c in range(cols):
    s.append(f'<text x="{bx+50+c*pitch}" y="{ry0-12}" font-size="10" fill="#666" text-anchor="middle">{c+1}</text>')
for r,lab in enumerate(rows):
    y = ry0 + r*pitch
    s.append(f'<text x="{bx+30}" y="{y+4}" font-size="11" fill="#666">{lab}</text>')
    for c in range(cols):
        s.append(f'<circle cx="{bx+50+c*pitch}" cy="{y}" r="3" fill="#8f8b80"/>')
# show one column's connectivity highlight
s.append(f'<rect x="{bx+50+12*pitch-8}" y="{ry0-9}" width="16" height="{4*pitch+18}" rx="4" fill="none" stroke="#c9a227" stroke-dasharray="3 2"/>')
s.append(f'<text x="{bx+50+12*pitch+4}" y="{ry0 + 4*pitch + 18 + 52}" font-size="10" fill="#8a6d00" text-anchor="end">↑ f~j 세로 5칸은 서로 연결 (13열 예시)</text>')
# center gutter
gy = ry0 + 4*pitch + 18
s.append(f'<rect x="{bx}" y="{gy}" width="{bw}" height="10" fill="#d8d4c8"/>')
s.append(f'<text x="{bx+bw/2}" y="{gy+9}" font-size="9" fill="#777" text-anchor="middle">가운데 홈 (여기서 끊김)</text>')
# lower block hint
for r,lab in enumerate(['e','d','c']):
    y = gy + 26 + r*pitch
    s.append(f'<text x="{bx+30}" y="{y+4}" font-size="11" fill="#aaa">{lab}</text>')
    for c in range(cols):
        s.append(f'<circle cx="{bx+50+c*pitch}" cy="{y}" r="3" fill="#c9c5b8"/>')

# ---------- module on f1..f8 ----------
fy = ry0 + 4*pitch
mx0 = bx+50
pins = ['VCC','GND','SCL','SDA','XDA','XCL','AD0','INT']
# header pins on f row
for c in range(8):
    s.append(f'<rect x="{mx0+c*pitch-3}" y="{fy-3}" width="6" height="6" fill="#222"/>')
# module body drawn as tilted-out board above, occupying j.. area visually? draw as a board hanging "outward" — simplify: board rectangle above f row overlapping header, semi-transparent
mby = fy-70
s.append(f'<rect x="{mx0-14}" y="{mby}" width="{8*pitch+6}" height="46" rx="4" fill="#2d5ba8" fill-opacity="0.92" stroke="#1b3d75"/>')
s.append(f'<text x="{mx0+4*pitch-8}" y="{mby+19}" font-size="12" fill="#fff" text-anchor="middle" font-weight="bold">GY-521 / MPU-6050</text>')
s.append(f'<rect x="{mx0+4*pitch-18}" y="{mby+24}" width="14" height="14" fill="#111"/>')
s.append(f'<text x="{mx0+4*pitch+2}" y="{mby+35}" font-size="9" fill="#dde">칩</text>')
for c,p in enumerate(pins):
    s.append(f'<line x1="{mx0+c*pitch}" y1="{mby+46}" x2="{mx0+c*pitch}" y2="{fy-3}" stroke="#999" stroke-width="2"/>')
    s.append(f'<text x="{mx0+c*pitch}" y="{fy+16}" font-size="8.5" fill="#333" text-anchor="middle">{p}</text>')
s.append(f'<text x="{mx0+8*pitch+8}" y="{mby+30}" font-size="10" fill="#333">← 모듈은 f1~f8 헤더에</text>')
s.append(f'<text x="{mx0+8*pitch+8}" y="{mby+43}" font-size="10" fill="#333">   얹어서 납땜</text>')

# ---------- Nucleo ----------
nx, ny = 600, 110
nw, nh = 300, 420
s.append(f'<rect x="{nx}" y="{ny}" width="{nw}" height="{nh}" rx="10" fill="#f2f4f7" stroke="#889"/>')
s.append(f'<text x="{nx+nw/2}" y="{ny-8}" font-size="13" fill="#555" text-anchor="middle">Nucleo-F446RE (위에서 본 모습, USB가 위쪽)</text>')
s.append(f'<rect x="{nx+nw/2-22}" y="{ny-2}" width="44" height="26" rx="3" fill="#bbb" stroke="#777"/>')
s.append(f'<text x="{nx+nw/2}" y="{ny+16}" font-size="9" fill="#333" text-anchor="middle">USB</text>')
s.append(f'<rect x="{nx+nw/2-30}" y="{ny+180}" width="60" height="60" fill="#333"/>')
s.append(f'<text x="{nx+nw/2}" y="{ny+214}" font-size="9" fill="#ddd" text-anchor="middle">STM32</text>')
# left header CN6 power (Arduino left side): NC, IOREF, RESET, 3V3, 5V, GND, GND, VIN
lx = nx+22; ly0 = ny+150
left = ['NC','IOREF','RESET','3.3V','5V','GND','GND','VIN']
s.append(f'<rect x="{lx-9}" y="{ly0-12}" width="18" height="{len(left)*18+6}" rx="3" fill="#111"/>')
s.append(f'<text x="{lx}" y="{ly0-18}" font-size="9" fill="#555" text-anchor="middle">CN6</text>')
lpos={}
for i,p in enumerate(left):
    y=ly0+i*18
    s.append(f'<circle cx="{lx}" cy="{y}" r="3.2" fill="#e0c060"/>')
    s.append(f'<text x="{lx+14}" y="{y+4}" font-size="10" fill="#333">{p}</text>')
    lpos[p+str(i)]=(lx,y)
# right header CN5 digital top: D15 SCL, D14 SDA, AREF, GND, D13 ...
rx_ = nx+nw-22; ry_0 = ny+60
right = ['D15 / SCL','D14 / SDA','AREF','GND','D13','D12','D11','D10','D9','D8']
s.append(f'<rect x="{rx_-9}" y="{ry_0-12}" width="18" height="{len(right)*18+6}" rx="3" fill="#111"/>')
s.append(f'<text x="{rx_}" y="{ry_0-18}" font-size="9" fill="#555" text-anchor="middle">CN5</text>')
rpos={}
for i,p in enumerate(right):
    y=ry_0+i*18
    s.append(f'<circle cx="{rx_}" cy="{y}" r="3.2" fill="#e0c060"/>')
    s.append(f'<text x="{rx_-14}" y="{y+4}" font-size="10" fill="#333" text-anchor="end">{p}</text>')
    rpos[p]=(rx_,y)

# ---------- wires: from g-row (row index 3) columns 1..4 ----------
gy_ = ry0 + 3*pitch
wires = [
    (0,'VCC', lpos['3.3V3'], '#d33', '3.3V'),
    (1,'GND', lpos['GND5'], '#222', 'GND'),
    (2,'SCL', rpos['D15 / SCL'], '#2a7', 'D15 (SCL)'),
    (3,'SDA', rpos['D14 / SDA'], '#27b', 'D14 (SDA)'),
]
for c,name,(tx,ty),col,lab in wires:
    x0 = mx0+c*pitch
    s.append(f'<circle cx="{x0}" cy="{gy_}" r="4" fill="{col}"/>')
    # route: up out of breadboard top area? go down below breadboard then across
    yb = by+bh+30+c*16
    if tx < nx+nw/2:   # left header: go down, across, up
        path = f'M{x0},{gy_} L{x0},{yb} L{tx-40-c*10},{yb} L{tx-40-c*10},{ty} L{tx},{ty}'
    else:              # right header: go down, across below nucleo?, up right side
        xr = nx+nw+30+(c-2)*14
        path = f'M{x0},{gy_} L{x0},{yb} L{xr},{yb} L{xr},{ty} L{tx},{ty}'
    s.append(f'<path d="{path}" fill="none" stroke="{col}" stroke-width="2.5" stroke-linejoin="round"/>')
    s.append(f'<text x="{x0+6}" y="{yb-4}" font-size="10" fill="{col}">g{c+1} ({name}) → {lab}</text>')

# legend
s.append(f'<text x="24" y="{H-40}" font-size="12" fill="#444">점퍼선은 암-수 케이블: 수(핀) 쪽을 브레드보드 g1~g4에, 암(구멍) 쪽을 Nucleo 검은 헤더에 꽂는다.  XDA·XCL·AD0·INT는 비워둔다.</text>')
s.append(f'<text x="24" y="{H-20}" font-size="12" fill="#444">D14/D15는 Nucleo 오른쪽 위 헤더(CN5)의 맨 위 두 핀. 3.3V·GND는 왼쪽 헤더(CN6). 5V에 꽂지 말 것.</text>')
s.append('</svg>')
svg = '\n'.join(s)
open('/mnt/user-data/outputs/wiring_mpu6050.svg','w').write(svg)
cairosvg.svg2png(bytestring=svg.encode(), write_to='/mnt/user-data/outputs/wiring_mpu6050.png', output_width=2200)
print('done')
