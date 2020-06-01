//*****************************************************************
/*
  JackTrip: A System for High-Quality Audio Network Performance
  over the Internet

  Copyright (c) 2020 Julius Smith, Juan-Pablo Caceres, Chris Chafe.
  SoundWIRE group at CCRMA, Stanford University.

  Permission is hereby granted, free of charge, to any person
  obtaining a copy of this software and associated documentation
  files (the "Software"), to deal in the Software without
  restriction, including without limitation the rights to use,
  copy, modify, merge, publish, distribute, sublicense, and/or sell
  copies of the Software, and to permit persons to whom the
  Software is furnished to do so, subject to the following
  conditions:

  The above copyright notice and this permission notice shall be
  included in all copies or substantial portions of the Software.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
  OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
  NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
  HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
  WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
  OTHER DEALINGS IN THE SOFTWARE.
*/
//*****************************************************************

/**
 * \file Limiter.cpp
 * \author Julius Smith, based on LoopBack.h
 * \date July 2008
 */


#include "Limiter.h"
#include "jacktrip_types.h"

#include <cstring> // for memcpy
#include <iostream>

//*******************************************************************************
void Limiter::compute(int nframes, float** inputs, float** outputs)
{
  static uint nSkippedFrames = 0;
  if (not inited) {
    nSkippedFrames++;
    if ((nSkippedFrames % 1000) == 1) {
      std::cout << "Limiter: compute() called before init(fs)\n";
      // it happens, so don't std::exit(1);
      if (nSkippedFrames>1) {
	std::cout << "Limiter: compute() called " << nSkippedFrames << " times before init(fs)\n";
      } else {
	if (fSamplingFreq <= 0) {
	  fSamplingFreq = 48000;
	  std::cout << "Limiter: *** GUESSED sampling rate to be 48000 Hz ***\n";
	}
	init(fSamplingFreq);
	inited = true; // It never comes!  Faust modules are presently mishandled
	std::cout << "Limiter: init done here now since it was found to never happen above\n";
      }
    }
  }
  for ( int i = 0; i < mNumClients; i++ ) {
    limiterP[i]->compute(nframes, inputs, outputs);
  }
}