#include "../indra/newview/oglnexversegridpolicy.h"
#include <cassert>
#include <string>
#include <iostream>

int main()
{
    using namespace OGLNexVerse;
    assert(std::string(GEN1_GRID) == "hg.stadt-nexverse.de");
    assert(std::string(GEN2_GRID) == "beta.stadt-nexverse.de");
    assert(!GEN2_ENABLED);
    assert(isAllowedGrid(GEN1_GRID));
    assert(!isAllowedGrid("nexverse")); // aliases must not create a second realm
    for (const auto& host : {
        "", "beta.stadt-nexverse.de", "secondlife.com",
        "hg.stadt-nexverse.de.evil.test", "evil.hg.stadt-nexverse.de",
        "http://hg.stadt-nexverse.de:80/", "HG.STADT-NEXVERSE.DE",
        "hg.stadt-nexverse.de:9001", "127.0.0.1", "localhost"})
        assert(!isAllowedGrid(host));
    assert(isAllowedLoginURI("http://hg.stadt-nexverse.de:80/"));
    for (const auto& uri : {
        "http://hg.stadt-nexverse.de/",
        "http://hg.stadt-nexverse.de:8002/",
        "http://hg.stadt-nexverse.de:80/?url=https://evil.test",
        "http://hg.stadt-nexverse.de:80/#fragment",
        "http://hg.stadt-nexverse.de:80/other",
        "https://hg.stadt-nexverse.de:80/",
        "http://user:password@hg.stadt-nexverse.de:80/",
        "http://hg.stadt-nexverse.de:80.evil.test/",
        "http://127.0.0.1:80/",
        "http://beta.stadt-nexverse.de:80/"})
        assert(!isAllowedLoginURI(uri));
    assert(isAllowedTravel("", "Magdeburg", false));
    assert(isAllowedTravel(GEN1_GRID, "Gummybear Island", false));
    assert(!isAllowedTravel(GEN2_GRID, "Magdeburg", false));
    assert(!isAllowedTravel("othergrid.example", "Magdeburg", false));
    assert(!isAllowedTravel(GEN1_GRID, "Magdeburg", true));
    assert(!isAllowedTravel(GEN1_GRID, "othergrid.example:9000:Region", false));
    assert(!isAllowedTravel(GEN1_GRID, "Region@othergrid.example", false));
    assert(!isAllowedTravel(GEN1_GRID, "https://foreign.example/region", false));
    std::cout << "TrixieStorm Gen1 login and travel policy tests passed\n";
}
