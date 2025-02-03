CXX = g++
CXXFLAGS = -Wall
LDFLAGS = -mwindows

BUILD_DIR = build
SRC_DIR = .
OUTPUT_DIR = ..

all: $(OUTPUT_DIR)/launcher.exe $(OUTPUT_DIR)/uninstall.exe

$(BUILD_DIR)/resources.o: $(SRC_DIR)/spotifylinker_resources.rc
	if not exist $(BUILD_DIR) mkdir $(BUILD_DIR)
	windres $(SRC_DIR)/spotifylinker_resources.rc -O coff -o $(BUILD_DIR)/resources.o

$(OUTPUT_DIR)/launcher.exe: $(BUILD_DIR)/resources.o $(SRC_DIR)/launcher.cpp
	$(CXX) $(CXXFLAGS) $(SRC_DIR)/launcher.cpp $(BUILD_DIR)/resources.o -o $(OUTPUT_DIR)/launcher.exe $(LDFLAGS)

$(OUTPUT_DIR)/uninstall.exe: $(BUILD_DIR)/resources.o $(SRC_DIR)/uninstall.c
	$(CXX) $(CXXFLAGS) $(SRC_DIR)/uninstall.c $(BUILD_DIR)/resources.o -o $(OUTPUT_DIR)/uninstall.exe $(LDFLAGS)

clean:
	if exist $(BUILD_DIR) rmdir /s /q $(BUILD_DIR)
	if exist $(OUTPUT_DIR)\launcher.exe del $(OUTPUT_DIR)\launcher.exe
	if exist $(OUTPUT_DIR)\uninstall.exe del $(OUTPUT_DIR)\uninstall.exe

.PHONY: all clean
