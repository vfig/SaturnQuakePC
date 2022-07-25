@echo off
set OUTPUT_DIR=%~dp0\..\io_mesh_saturnlev
call kaitai-struct-compiler -t python -d %OUTPUT_DIR% dat_skank.ksy
call kaitai-struct-compiler -t python -d %OUTPUT_DIR% lev_duke.ksy
call kaitai-struct-compiler -t python -d %OUTPUT_DIR% lev_powerslave.ksy
call kaitai-struct-compiler -t python -d %OUTPUT_DIR% lev_powerslave_psx.ksy
call kaitai-struct-compiler -t python -d %OUTPUT_DIR% lev_quake.ksy
