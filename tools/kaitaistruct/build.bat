@echo off
set OUTPUT_DIR=%~dp0\..\io_mesh_saturnlev
call kaitai-struct-compiler -t python -d %OUTPUT_DIR% qslev.ksy
call kaitai-struct-compiler -t python -d %OUTPUT_DIR% powerslavelev.ksy
call kaitai-struct-compiler -t python -d %OUTPUT_DIR% dukelev.ksy
