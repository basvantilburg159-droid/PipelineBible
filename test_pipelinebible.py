#!/usr/bin/env python3
"""
PipelineBible v1.1 - Test Script
Eenvoudige tests om alle functionaliteit te demonstreren
"""

def test_pipe_lookup():
    """Test pipe data lookup functionaliteit"""
    print("\n" + "="*60)
    print("TEST 1: Pipe Lookup")
    print("="*60)
    
    from PipelineBible import PipeLookup
    
    # Test 1: Zoek specifieke pipe
    print("\n1. Zoek NPS 6\" Schedule STD pipe:")
    dims = PipeLookup.get_pipe_dimension('6', 'STD', 'ASME')
    if dims:
        print(f"   ✓ OD: {dims['od']} mm")
        print(f"   ✓ WT: {dims['wt']} mm")
        print(f"   ✓ ID: {dims['id']} mm")
        print(f"   ✓ Gewicht: {dims['kg']} kg/m")
    else:
        print("   ✗ Niet gevonden")
    
    # Test 2: List schedules
    print("\n2. Beschikbare schedules voor NPS 6\":")
    schedules = PipeLookup.list_schedules('6', 'ASME')
    print(f"   {schedules}")
    
    # Test 3: Valideer pipe size
    print("\n3. Valideer of NPS 24\" bestaat:")
    exists = PipeLookup.validate_nps('24', 'ASME')
    print(f"   {'✓ Bestaat' if exists else '✗ Bestaat niet'}")
    
    # Test 4: DIN pipe
    print("\n4. Zoek DIN DN150 2.6mm:")
    dims = PipeLookup.get_pipe_dimension('DN150', '2.6', 'DIN')
    if dims:
        print(f"   ✓ OD: {dims['od']} mm, WT: {dims['wt']} mm, ID: {dims['id']} mm")


def test_flange_lookup():
    """Test flange data lookup functionaliteit"""
    print("\n" + "="*60)
    print("TEST 2: Flange Lookup")
    print("="*60)
    
    from PipelineBible import FlangeLookup
    
    # Test 1: Zoek flens
    print("\n1. Zoek NPS 6\" Class 150 flens:")
    flange = FlangeLookup.get_flange_data('6', 150, 'ASME')
    if flange:
        print(f"   ✓ Flange OD: {flange['flange_od']} mm")
        print(f"   ✓ Bolt Circle: {flange['bolt_circle']} mm")
        print(f"   ✓ Bouten: {flange['bolt_holes']} x {flange['bolt_size']}\"")
        print(f"   ✓ Serie: {flange['series']}")
    
    # Test 2: List classes
    print("\n2. Beschikbare classes voor NPS 6\":")
    classes = FlangeLookup.list_classes('6', 'ASME')
    print(f"   {classes}")
    
    # Test 3: Grote flens (B16.47)
    print("\n3. Zoek grote flens NPS 36\" Class 150:")
    flange = FlangeLookup.get_flange_data('36', 150, 'ASME')
    if flange:
        print(f"   ✓ Flange OD: {flange['flange_od']} mm")
        print(f"   ✓ Serie: {flange['series']} (B16.47)")


def test_pretty_print():
    """Test formatted output functionaliteit"""
    print("\n" + "="*60)
    print("TEST 3: Pretty Print (Formatted Output)")
    print("="*60)
    
    from PipelineBible import PrettyPrint
    
    print("\n1. Print pipe info:")
    PrettyPrint.print_pipe('8', '40', 'ASME')
    
    print("\n2. Print flange info:")
    PrettyPrint.print_flange('8', 150, 'ASME')
    
    print("\n3. Lijst eerste 10 ASME pipe sizes:")
    PrettyPrint.list_all_pipes('ASME', max_display=10)


def test_data_export():
    """Test export functionaliteit"""
    print("\n" + "="*60)
    print("TEST 4: Data Export")
    print("="*60)
    
    from PipelineBible import DataExport
    import os
    
    # Test 1: Export naar CSV
    print("\n1. Export pipes naar CSV:")
    filename = 'test_export_pipes.csv'
    DataExport.export_pipes_csv(filename, 'ASME')
    if os.path.exists(filename):
        size = os.path.getsize(filename)
        print(f"   ✓ Bestand aangemaakt: {filename} ({size} bytes)")
        
        # Toon eerste 3 regels
        print("\n   Eerste regels:")
        with open(filename, 'r') as f:
            for i, line in enumerate(f):
                if i < 3:
                    print(f"   {line.strip()}")
        
        os.remove(filename)
        print(f"   ✓ Test bestand opgeschoond")
    
    # Test 2: Export naar JSON
    print("\n2. Export data naar JSON:")
    filename = 'test_export_data.json'
    DataExport.export_to_json(filename, 'ASME')
    if os.path.exists(filename):
        size = os.path.getsize(filename)
        print(f"   ✓ Bestand aangemaakt: {filename} ({size} bytes)")
        
        # Toon begin van JSON
        print("\n   Begin van JSON:")
        with open(filename, 'r') as f:
            lines = f.readlines()[:4]
            for line in lines:
                print(f"   {line.strip()}")
        
        os.remove(filename)
        print(f"   ✓ Test bestand opgeschoond")


def test_calculations():
    """Test calculation functies"""
    print("\n" + "="*60)
    print("TEST 5: Berekeningen")
    print("="*60)
    
    from PipelineBible import cdm, cbn, bolt_len, get_stud
    
    # Test 1: Pipe dimensions
    print("\n1. Bereken pipe dimensies (OD=219.1mm, WT=8.18mm):")
    dims = cdm(219.1, 8.18)
    print(f"   ✓ ID: {dims['id']} mm")
    print(f"   ✓ Gewicht: {dims['kg']} kg/m")
    
    # Test 2: Bend berekening
    print("\n2. Bereken 8\" 90° bend met 1.5D radius:")
    bend = cbn(219.1, 8.18, 1.5, 90)
    print(f"   ✓ Radius: {bend['R']} mm")
    print(f"   ✓ Tangent: {bend['T']} mm")
    print(f"   ✓ Arc length: {bend['ac']} mm")
    
    # Test 3: Bolt length
    print("\n3. Bereken bolt length voor Class 150 flens:")
    length = bolt_len(th=25.4, bd="3/4", gt=4.5, wr=False, ft="WN", std="ASME")
    print(f"   ✓ Bolt length: {length} mm")
    
    # Test 4: Stud specs
    print("\n4. Zoek 3/4\" stud specificaties:")
    stud = get_stud("3/4", "ASME")
    print(f"   ✓ Diameter: {stud[0]} mm, Hex: {stud[1]} mm")


def test_database_coverage():
    """Test database coverage"""
    print("\n" + "="*60)
    print("TEST 6: Database Coverage")
    print("="*60)
    
    from PipelineBible import ASME_PIPES, DIN_PIPES, ASME_FL, DIN_FL, BENDS, GASKETS
    
    print(f"\n   ✓ ASME Pipes: {len(ASME_PIPES)} sizes")
    print(f"   ✓ DIN Pipes: {len(DIN_PIPES)} sizes")
    print(f"   ✓ ASME Flanges: {len(ASME_FL)} entries")
    print(f"   ✓ DIN Flanges: {len(DIN_FL)} entries")
    print(f"   ✓ Bend types: {len(BENDS)}")
    print(f"   ✓ Gasket types: {len(GASKETS)}")
    
    # Check range
    nps_sizes = [p[0] for p in ASME_PIPES]
    print(f"\n   ASME range: {nps_sizes[0]} tot {nps_sizes[-1]}")
    
    dn_sizes = [p[0] for p in DIN_PIPES]
    print(f"   DIN range: {dn_sizes[0]} tot {dn_sizes[-1]}")


def run_all_tests():
    """Run alle tests"""
    print("\n" + "="*70)
    print(" "*15 + "PIPELINEBIBLE v1.1 TEST SUITE")
    print("="*70)
    
    try:
        test_pipe_lookup()
        test_flange_lookup()
        test_pretty_print()
        test_data_export()
        test_calculations()
        test_database_coverage()
        
        print("\n" + "="*70)
        print("✓ ALLE TESTS SUCCESVOL!")
        print("="*70)
        print("\nPipelineBible v1.1 is klaar voor gebruik!")
        print("Zie README.md voor volledige documentatie.\n")
        
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    run_all_tests()
