import wave        
import struct
import sys

def lsb_watermark(cover_filepath, watermark_data, watermarked_output_path):
    watermark_str = str(watermark_data)
    #chuyen sang ma accsi o->111
    watermark = struct.unpack("%dB" % len(watermark_str), watermark_str)
    watermark_size = len(watermark)
    watermark_bits = watermark_to_bits((watermark_size,), 32)
    watermark_bits.extend(watermark_to_bits(watermark))
    

    cover_audio = wave.open(cover_filepath, 'rb') 
    #kenh, chieu rong, tan xuat, so tan xuat, kieu du lieu,phien ban
    (nchannels, sampwidth, framerate, nframes, comptype, compname) = cover_audio.getparams()
    #doc nframes * nchannels byte trong file
    frames = cover_audio.readframes (nframes * nchannels)
    #chyen sang hex voi 32bit
    samples = struct.unpack_from ("%dh" % nframes * nchannels, frames)
    if len(samples) < len(watermark_bits):
        raise OverflowError("Du lieu giau trong file qua lon so voi dung luong file! dung luong du lieu la: %d con dung luong file la: %d bits of space." % (len(watermark_bits), len(samples))) 
    
    encoded_samples = []
    
    watermark_position = 0
    n = 0
    for sample in samples:
        encoded_sample = sample
        
        if watermark_position < len(watermark_bits):
            encode_bit = watermark_bits[watermark_position]
            if encode_bit == 1:
                encoded_sample = sample | encode_bit
            else:
                encoded_sample = sample
                if sample & 1 != 0:
                    encoded_sample = sample - 1
                    
            watermark_position = watermark_position + 1
            
        encoded_samples.append(encoded_sample)
    #ghi vao file       
    encoded_audio = wave.open(watermarked_output_path, 'wb')
    encoded_audio.setparams( (nchannels, sampwidth, framerate, nframes, comptype, compname) )

    encoded_audio.writeframes(struct.pack("%dh" % len(encoded_samples), *encoded_samples))

def watermark_to_bits(watermark, nbits=8):
    watermark_bits = []
    for byte in watermark:
        for i in range(0,nbits):
            watermark_bits.append( (byte & (2 ** i)) >> i )
    return watermark_bits
    
def recover_lsb_watermark(watermarked_filepath):
    watermarked_audio = wave.open(watermarked_filepath, 'rb') 
    #kenh, bien do,,3:tan so trich mau
    (nchannels, sampwidth, framerate, nframes, comptype, compname) = watermarked_audio.getparams()
    frames = watermarked_audio.readframes (nframes * nchannels)
    samples = struct.unpack_from ("%dh" % nframes * nchannels, frames)
    
    watermark_bytes = 0
    for (sample,i) in zip(samples[0:32], range(0,32)):
        watermark_bytes = watermark_bytes + ( (sample & 1) * (2 ** i))
    
    watermark_data = ""
    
    for n in range(0, watermark_bytes):
        watermark_byte_samples = samples[32 + (n * 8) : 32+((n+1) * 8)]
        watermark_byte = 0
        for (sample, i) in zip(watermark_byte_samples, range(0,8)):
            watermark_byte = watermark_byte + ( (sample & 1) * (2**i) )
        watermark_data=watermark_data + chr(watermark_byte)
            
    return watermark_data
    
def watermark_to_string(list):
    return "".join([chr(x) for x in list])

    #lsb_watermark(cover_audio, message, output)
    
#recover_lsb_watermark("nam.wav") 
