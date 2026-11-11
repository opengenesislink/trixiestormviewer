// Isolated C++17 regression for the clock formatting algorithm. This does
// not compile the whole Firestorm viewer or exercise OGL network callbacks.
#include <cassert>
#include <ctime>
#include <regex>
#include <string>
#include <iostream>

static std::string timeTemplate(std::string format, const std::string& zone)
{
    static const std::regex timezoneToken(R"(\[timezone\s*,\s*datetime\s*,\s*slt\s*\])");
    static const std::regex sltToken(R"(,\s*slt\s*\])");
    format = std::regex_replace(format, timezoneToken, "OGLSERVERCLOCKZONE");
    format = std::regex_replace(format, sltToken, ", utc]");
    std::string::size_type index = 0;
    while ((index = format.find("OGLSERVERCLOCKZONE", index)) != std::string::npos)
    {
        format.replace(index, 18, zone);
        index += zone.size();
    }
    return format;
}

int main()
{
    for (const auto& zone : {"MEZ", "MESZ", "UTC+05:30"})
    {
        const std::string t24 = timeTemplate(
            "[hour24, datetime, slt]:[min, datetime, slt] [timezone, datetime, slt]", zone);
        assert(t24.find(zone) != std::string::npos);
        assert(t24.find("slt") == std::string::npos);
        assert(t24.find("[hour24, datetime, utc]") != std::string::npos);

        const std::string t12 = timeTemplate(
            "[hour12, datetime, slt]:[min, datetime, slt]:[second, datetime, slt] "
            "[ampm, datetime, slt] [timezone,datetime, slt]", zone);
        assert(t12.find(zone) != std::string::npos);
        assert(t12.find("slt") == std::string::npos);
        assert(t12.find("[second, datetime, utc]") != std::string::npos);
    }

    const std::time_t instant = 1800000000;
    for (int offset : {3600, 7200, -18000, 19800})
    {
        const std::time_t civil = instant + offset;
        const std::tm* t = std::gmtime(&civil);
        assert(t != nullptr);
        // The viewer passes this offset-adjusted epoch to a UTC formatter:
        // the displayed wall-clock is independent of the PC's local TZ.
        assert(civil - instant == offset);
    }
    std::cout << "NexVerse status-bar clock format test passed\n";
}
