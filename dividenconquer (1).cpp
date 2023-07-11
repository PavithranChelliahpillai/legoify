#include <bits/stdc++.h>
using namespace std;

typedef vector<vector<bool>> vvb;
typedef vector<vector<int>> vvi;
typedef pair<int, int> pi;

set<pi> base;
int bricks[2000][2000];

int ans = 0;

vvb loadBooleanArrayFromFile(const string& filename) {
    ifstream file(filename);
    vvb booleanArray;
    string line;

    while (getline(file, line)) {
        vector<bool> row;
        for (char c : line) {
            row.push_back(c == '1');
        }
        booleanArray.push_back(row);
    }

    return booleanArray;
}

void divconquer(vvb a, vvi psa, int minx, int miny, int maxx, int maxy) {
    int width = maxx - minx + 1, height = maxy - miny + 1;
    // check base cases
    if (width == 1 && height == 1) return;

    if (base.find({min(width, height), max(width, height)}) != base.end()) {
        int area = width * height, real;
        real = psa[maxx][maxy] - psa[maxx][miny - 1] - psa[minx - 1][maxy] + psa[minx - 1][miny - 1];
        float thresh = (float) real / area;

        if (thresh >= 0.5) {
            ans++;
            // cout << miny << ',' << minx << ',' << maxy << ',' << maxx << endl;
            bricks[minx][miny] += ans;
            bricks[minx][maxy + 1] += -ans;
            bricks[maxx + 1][miny] += -ans;
            bricks[maxx + 1][maxy + 1] += ans;
            return;
        }
    }

    if (height > width) {
        divconquer(a, psa, minx, miny, maxx, (int)(miny + maxy) / 2);
        divconquer(a, psa, minx, (int)(miny + maxy) / 2 + 1, maxx, maxy);
    } else {
        divconquer(a, psa, minx, miny, (int)(minx + maxx) / 2, maxy);
        divconquer(a, psa, (int)(minx + maxx) / 2 + 1, miny, maxx, maxy);
    }
}

void solve(vvb a) {
    memset(bricks, 0, sizeof(bricks));
    // calculate bounding box, make psa, prelim work
    vvi psa(a.size(), vector<int>(a[0].size(), 0)); // Size the psa vector to match the dimensions of the boolean array 'a'
    int minx = 1e9, miny = 1e9, maxx = -1, maxy = -1;
    for (int i = 0; i < a.size(); i++) {
        for (int j = 0; j < a[i].size(); j++) {
            psa[i][j] = a[i][j];
            if (!a[i][j]) continue;
            minx = min(minx, i); maxx = max(maxx, i);
            miny = min(miny, j); maxy = max(maxy, j);
        }
    }
    for (int i = 1; i < a.size(); i++) {
        for (int j = 1; j < a[i].size(); j++) {
            psa[i][j] += psa[i - 1][j] + psa[i][j - 1] - psa[i - 1][j - 1];
        }
    }
    divconquer(a, psa, minx, miny, maxx, maxy);
}

void saveBricksToFile(const string& folderPath, const string& filenamePrefix, int bricks[][2000], int sizeX, int sizeY, int fileNumber) {
    string folderName = folderPath + "/solutions";
    filesystem::create_directories(folderName); 
    string filename = folderName + "/" + filenamePrefix + std::to_string(fileNumber) + ".txt";
    ofstream file(filename);

    if (!file) {
        cout << "Error opening file " << filename << endl;
        return;
    }

    for (int i = 0; i < sizeX; i++) {
        for (int j = 0; j < sizeY; j++) {
            file << bricks[i][j] << " ";
        }
        file << endl;
    }

    file.close();
}

int main() {
    string folderPath = "/home/pchellia/Desktop/Legoify/bnw_slices";
    string solutionsFolderPath = "/home/pchellia/Desktop/Legoify/solutions"; 
    base.insert({1, 4});
    base.insert({1, 3});
    base.insert({1, 2});
    base.insert({2, 2});
    base.insert({2, 3}); 
    base.insert({2, 4});

    int fileNumber = 1;

    for (const auto& entry : filesystem::directory_iterator(folderPath)) {
        if (entry.path().extension() == ".txt") {
            string filename = entry.path().filename();
            vvb booleanArray = loadBooleanArrayFromFile(entry.path().string());
            ans = 0;
            memset(bricks, 0, sizeof(bricks));
            solve(booleanArray);
            cout << filename << ':' << ans << endl;

            for (int i = 1; i < 2000; i++) {
                for (int j = 0; j < 2000; j++) {
                    bricks[i][j] += bricks[i - 1][j];
                }
            }
            for (int i = 0; i < 2000; i++) {
                for (int j = 1; j < 2000; j++) {
                    bricks[i][j] += bricks[i][j - 1];
                }
            }

            if (!filesystem::exists(solutionsFolderPath)) {
                filesystem::create_directory(solutionsFolderPath);
            }

            saveBricksToFile(solutionsFolderPath, "bricks", bricks, 2000, 2000, fileNumber);
            fileNumber++;
        }
    }

    cout << "All files processed." << endl;

    return 0;
}
