
			class lev_planeflags(Flag):
				LAVA = 1
				UN2 = 2
				UN3 = 4
				TOUCHABLE = 8
				UN4 = 16
				UN5 = 32
				UN6 = 64
				UN7 = 128
				VISIBLE = 256
				LIQUID = 512
				UN8 = 1024
				UN9 = 2048
				UN10 = 4096
				SLIME = 8192

				# LAVA surface = 384 = 256 + 128 + 1
				# LAVA volume = 641 = 512 + 128 + 1
				# WATER volume = 512 = 512
				# SLIME volume = 8704 = 8192 + 512